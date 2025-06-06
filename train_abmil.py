# import enum
# import re
# from symbol import testlist_star_expr
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
# from torch.autograd import Variable
# import torchvision.transforms.functional as VF
# from torchvision import transforms

import sys, argparse, os, copy, itertools, glob, datetime
import pandas as pd
import numpy as np
# from sklearn.utils import shuffle
# from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_fscore_support, classification_report
# from sklearn.datasets import load_svmlight_file
# from collections import OrderedDict
from torch.utils.data import Dataset
import redis
import pickle
import time
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, \
    roc_auc_score, roc_curve
import random
import torch.backends.cudnn as cudnn
import json
# torch.multiprocessing.set_sharing_strategy('file_system')
import os
import joblib
from torch.cuda.amp import GradScaler, autocast



class BagDataset(Dataset):
    def __init__(self, train_path, args) -> None:
        super(BagDataset).__init__()
        self.train_path = train_path
        self.args = args
        # self.database = redis.Redis(host='localhost', port=6379)

    def get_bag_feats(self, csv_file_df, args):
        # if args.dataset == 'TCGA-lung-default':
        #     feats_csv_path = 'datasets/tcga-dataset/tcga_lung_data_feats/' + csv_file_df.iloc[0].split('/')[1] + '.csv'
        if args.dataset.startswith('tcga'):
            feats_csv_path = os.path.join('datasets', args.dataset, 'data_tcga_lung_tree',
                                          csv_file_df.iloc[0].split('/')[-1] + '.csv')
        else:
            feats_csv_path = csv_file_df.iloc[0]

        # key = csv_file_df.iloc[0]
        # feats = pickle.loads(self.database.get(key+'feats'))
        # label = pickle.loads(self.database.get(key+'label'))
        # return label, feats
        # df = pd.read_csv(feats_csv_path)
        # feats = shuffle(df).reset_index(drop=True)
        # feats = feats.to_numpy()
        feats = torch.load(feats_csv_path)
        label = np.zeros(args.num_classes)
        if args.num_classes == 1:
            label[0] = csv_file_df.iloc[1]
        else:
            if int(csv_file_df.iloc[1]) <= (len(label) - 1):
                label[int(csv_file_df.iloc[1])] = 1
        label = torch.tensor(np.array(label))
        feats = torch.tensor(np.array(feats)).float()
        return label, feats

    def dropout_patches(self, feats, p):
        idx = np.random.choice(np.arange(feats.shape[0]), int(feats.shape[0] * (1 - p)), replace=False)
        sampled_feats = np.take(feats, idx, axis=0)
        pad_idx = np.random.choice(np.arange(sampled_feats.shape[0]), int(feats.shape[0] * p), replace=False)
        pad_feats = np.take(sampled_feats, pad_idx, axis=0)
        sampled_feats = np.concatenate((sampled_feats, pad_feats), axis=0)
        return sampled_feats

    def __getitem__(self, idx):
        label, feats = self.get_bag_feats(self.train_path.iloc[idx], self.args)
        return label, feats

    def __len__(self):
        return len(self.train_path)


def train(train_df, milnet, criterion, optimizer, args, log_path, epoch,scaler):
    milnet.train()
    total_loss = 0
    atten_max = 0
    atten_min = 0
    atten_mean = 0

    for i, (bag_label, bag_feats) in enumerate(train_df):
        torch.cuda.empty_cache()
        bag_label = bag_label.cuda()
        bag_feats = bag_feats.cuda()
        bag_feats = bag_feats.view(-1, args.feats_size)  # n x feat_dim
        optimizer.zero_grad()
        with autocast():
            bag_prediction, _, attention = milnet(bag_feats)
            loss = criterion(bag_prediction.view(1, -1), bag_label.view(1, -1))

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        total_loss = total_loss + loss.item()
        atten_max = atten_max + attention.max().item()
        atten_min = atten_min + attention.min().item()
        atten_mean = atten_mean + attention.mean().item()

        sys.stdout.write('\r Training bag [%d/%d] bag loss: %.4f, attention max:%.4f, min:%.4f, mean:%.4f' % (
        i, len(train_df), loss.item(),
        attention.max().item(), attention.min().item(), attention.mean().item()))
    atten_max = atten_max / len(train_df)
    atten_min = atten_min / len(train_df)
    atten_mean = atten_mean / len(train_df)
    with open(log_path, 'a+') as log_txt:
        log_txt.write('\n atten_max' + str(atten_max))
        log_txt.write('\n atten_min' + str(atten_min))
        log_txt.write('\n atten_mean' + str(atten_mean))
    return total_loss / len(train_df)


def test(test_df, milnet, criterion, optimizer, args, log_path, epoch):
    milnet.eval()
    total_loss = 0
    test_labels = []
    test_predictions = []
    Tensor = torch.cuda.FloatTensor
    with torch.no_grad():
        for i, (bag_label, bag_feats) in enumerate(test_df):
            torch.cuda.empty_cache()
            label = bag_label.numpy()
            bag_label = bag_label.cuda()
            bag_feats = bag_feats.cuda()
            bag_feats = bag_feats.view(-1, args.feats_size)
            # if args.model == 'dsmil':
            #     ins_prediction, bag_prediction, _, _ = milnet(bag_feats)
            #     max_prediction, _ = torch.max(ins_prediction, 0)
            #     bag_loss = criterion(bag_prediction.view(1, -1), bag_label.view(1, -1))
            #     max_loss = criterion(max_prediction.view(1, -1), bag_label.view(1, -1))
            #     # bag_loss = criterion(bag_prediction, bag_label.long())
            #     # max_loss = criterion(max_prediction.view(1, -1), bag_label.long())
            #     loss = 0.5 * bag_loss + 0.5 * max_loss
            # elif args.model in ['abmil', 'max', 'mean']:
            with autocast():
                bag_prediction, _, _ = milnet(bag_feats)
                max_prediction = bag_prediction
                loss = criterion(bag_prediction.view(1, -1), bag_label.view(1, -1))
                total_loss = total_loss + loss.item()
                sys.stdout.write('\r Testing bag [%d/%d] bag loss: %.4f' % (i, len(test_df), loss.item()))
                test_labels.extend(label)
                test_predictions.extend([torch.sigmoid(bag_prediction).squeeze().cpu().numpy()])
                # if args.average:  # notice args.average here
                #     test_predictions.extend([(0.5 * torch.sigmoid(max_prediction) + 0.5 * torch.sigmoid(
                #         bag_prediction)).squeeze().cpu().numpy()])
                #
                # else:
                #     test_predictions.extend([(0.0 * torch.sigmoid(max_prediction) + 1.0 * torch.sigmoid(
                #         bag_prediction)).squeeze().cpu().numpy()])
    test_labels = np.array(test_labels)
    test_predictions = np.array(test_predictions)

    auc_value, _, thresholds_optimal = multi_label_roc(test_labels, test_predictions, args.num_classes, pos_label=1)
    with open(log_path, 'a+') as log_txt:
        log_txt.write('\n *****************Threshold by optimal*****************')
    if args.num_classes == 1:
        class_prediction_bag = copy.deepcopy(test_predictions)
        class_prediction_bag[test_predictions >= thresholds_optimal[0]] = 1
        class_prediction_bag[test_predictions < thresholds_optimal[0]] = 0
        test_predictions = class_prediction_bag
        test_labels = np.squeeze(test_labels)
        print('\n')
        print(confusion_matrix(test_labels, test_predictions))
        info = confusion_matrix(test_labels, test_predictions)
        with open(log_path, 'a+') as log_txt:
            log_txt.write('\n' + str(info))
    else:
        for i in range(args.num_classes):
            class_prediction_bag = copy.deepcopy(test_predictions[:, i])
            class_prediction_bag[test_predictions[:, i] >= thresholds_optimal[i]] = 1
            class_prediction_bag[test_predictions[:, i] < thresholds_optimal[i]] = 0
            test_predictions[:, i] = class_prediction_bag
            print(confusion_matrix(test_labels[:, i], test_predictions[:, i]))
            info = confusion_matrix(test_labels[:, i], test_predictions[:, i])
            with open(log_path, 'a+') as log_txt:
                log_txt.write('\n' + str(info))
    bag_score = 0
    # average acc of all labels
    for i in range(0, len(test_df)):
        bag_score = np.array_equal(test_labels[i], test_predictions[i]) + bag_score
    avg_score = bag_score / len(test_df)  # ACC
    cls_report = classification_report(test_labels, test_predictions, digits=4)
    print('\n  multi-label Accuracy:{:.2f}, AUC:{:.2f}'.format(avg_score * 100, sum(auc_value) / len(auc_value) * 100))
    print('\n', cls_report)
    with open(log_path, 'a+') as log_txt:
        log_txt.write(
            '\n multi-label Accuracy:{:.2f}, AUC:{:.2f}'.format(avg_score * 100, sum(auc_value) / len(auc_value) * 100))
        log_txt.write('\n' + cls_report)
    return total_loss / len(test_df), avg_score, auc_value, thresholds_optimal


def multi_label_roc(labels, predictions, num_classes, pos_label=1):
    fprs = []
    tprs = []
    thresholds = []
    thresholds_optimal = []
    aucs = []
    if len(predictions.shape) == 1:
        predictions = predictions[:, None]
    for c in range(0, num_classes):
        label = labels[:, c]
        if sum(label) == 0:
            continue
        prediction = predictions[:, c]
        fpr, tpr, threshold = roc_curve(label, prediction, pos_label=1)
        fpr_optimal, tpr_optimal, threshold_optimal = optimal_thresh(fpr, tpr, threshold)
        c_auc = roc_auc_score(label, prediction)
        aucs.append(c_auc)
        thresholds.append(threshold)
        thresholds_optimal.append(threshold_optimal)
    return aucs, thresholds, thresholds_optimal


def optimal_thresh(fpr, tpr, thresholds, p=0):
    loss = (fpr - tpr) - p * tpr / (fpr + tpr + 1)
    idx = np.argmin(loss, axis=0)
    return fpr[idx], tpr[idx], thresholds[idx]


def main():
    parser = argparse.ArgumentParser(description='Train IBMIL for abmil and dsmil')
    parser.add_argument('--num_classes', default=2, type=int, help='Number of output classes [2]')
    parser.add_argument('--feats_size', default=768, type=int, help='Dimension of the feature size [512]')
    parser.add_argument('--lr', default=0.0001, type=float, help='Initial learning rate [0.0002]')
    parser.add_argument('--num_epochs', default=50, type=int, help='Number of total training epochs [40|200]')
    parser.add_argument('--gpu_index', type=int, nargs='+', default=(0,), help='GPU ID(s) [0]')
    parser.add_argument('--gpu', type=str, default='0')
    parser.add_argument('--weight_decay', default=1e-4, type=float, help='Weight decay [5e-3]')
    parser.add_argument('--weight_decay_conf', default=1e-4, type=float, help='Weight decay [5e-3]')
    parser.add_argument('--dataset', default='danzhiyuji', type=str, help='Dataset folder name')
    parser.add_argument('--split', default=0.2, type=float, help='Training/Validation split [0.2]')
    parser.add_argument('--model', default='abmil', type=str, help='MIL model [abmil, dsmil]')
    parser.add_argument('--dropout_patch', default=0.1, type=float, help='Patch dropout rate [0]')
    parser.add_argument('--dropout_node', default=0, type=float, help='Bag classifier dropout rate [0]')
    parser.add_argument('--non_linearity', default=0, type=float, help='Additional nonlinear operation [0]')
    parser.add_argument('--average', type=bool, default=True,
                        help='Average the score of max-pooling and bag aggregating')
    parser.add_argument('--test', action='store_true', help='Test only')
    parser.add_argument('--seed', default=None, type=int, help='seed for initializing training. ')
    parser.add_argument('--agg', type=str, help='which agg')
    parser.add_argument('--c_path', nargs='+',
                        default=None, type=str,
                        help='directory to confounders')#'./datasets_deconf/STAS/train_bag_cls_agnostic_feats_proto_8_dsmil.npy'
    # for ablations only
    parser.add_argument('--c_learn', action='store_true', help='learn confounder or not')
    parser.add_argument('--c_dim', default=128, type=int, help='Dimension of the projected confounders')
    parser.add_argument('--freeze_epoch', default=999, type=int,
                        help='freeze confounders during this many epoch from the start')
    parser.add_argument('--c_merge', type=str, default='cat', help='cat or add or sub')
    args = parser.parse_args()

    # logger
    arg_dict = vars(args)
    dict_json = json.dumps(arg_dict)
    if args.c_path:
        save_path = os.path.join('deconf', datetime.date.today().strftime("%m%d%Y"),
                                 str(args.dataset) + '_' + str(args.model) + '_' + str(args.agg) + '_c_path')
    else:
        save_path = os.path.join('baseline', datetime.date.today().strftime("%m%d%Y"),
                                 str(args.dataset) + '_' + str(args.model) + '_' + str(args.agg) + '_fulltune')
    run = len(glob.glob(os.path.join(save_path, '*')))
    save_path = os.path.join(save_path, str(run))
    os.makedirs(save_path, exist_ok=True)
    save_file = save_path + '/config.json'
    with open(save_file, 'w+') as f:
        f.write(dict_json)
    log_path = save_path + '/log.txt'

    # seed
    if args.seed is not None:
        random.seed(args.seed)
        torch.manual_seed(args.seed)
        cudnn.deterministic = True

    '''
    model 
    1. set require_grad    
    2. choose model and set the trainable params 
    3. load init
    '''
    if args.model == 'dsmil':
        import Models.dsmil as mil
        i_classifier = mil.FCLayer(in_size=args.feats_size, out_size=args.num_classes).cuda()
        b_classifier = mil.BClassifier(input_size=args.feats_size, output_class=args.num_classes,
                                       dropout_v=args.dropout_node, nonlinear=args.non_linearity,
                                       confounder_path=args.c_path).cuda()
        milnet = mil.MILNet(i_classifier, b_classifier).cuda()

    elif args.model == 'abmil':
        import Models.abmil as mil
        milnet = mil.Attention(in_size=args.feats_size, out_size=args.num_classes, confounder_path=args.c_path, \
                               confounder_learn=args.c_learn, confounder_dim=args.c_dim,
                               confounder_merge=args.c_merge).cuda()

    for name, _ in milnet.named_parameters():
        print('Training {}'.format(name))
        with open(log_path, 'a+') as log_txt:
            log_txt.write('\n Training {}'.format(name))

    if args.dataset.startswith("LUAD"):
        bags_csv = os.path.join('datasets_csv', args.dataset + '.csv')
        bags_path = pd.read_csv(bags_csv)
        loss_weight = torch.tensor([[1]]).cuda()
        # bags_csv = os.path.join('datasets', args.dataset, args.dataset + '.csv')
        # bags_path = pd.read_csv(bags_csv)
        # train_path = bags_path.iloc[0:int(len(bags_path) * 0.8), :]
        # test_path = bags_path.iloc[int(len(bags_path) * 0.8):, :]


    elif args.dataset.startswith('danzhiyuji'):
        # bags_csv = os.path.join('datasets', args.dataset, args.dataset+'_off.csv') #offical train test
        bags_csv = os.path.join('data_csv', args.dataset + '.csv')
        bags_path = pd.read_csv(bags_csv)
        loss_weight = torch.tensor([[1]]).cuda()

    print(milnet)
    scaler = GradScaler()
    # 遍历每个折数进行训练
    for fold in range(5):
        with open(log_path, 'a+') as log_txt:
            info = '\n' + 'Fold at: ' + str(fold) + '\n'
            log_txt.write(info)
        print('Fold at: ' + str(fold))
        train_path = (bags_path[bags_path['Fold'] != fold]).drop(columns=['Fold'])
        test_path = (bags_path[bags_path['Fold'] == fold]).drop(columns=['Fold'])

        trainset = BagDataset(train_path, args)
        train_loader = DataLoader(trainset, 1, shuffle=True, num_workers=0)
        testset = BagDataset(test_path, args)
        test_loader = DataLoader(testset, 1, shuffle=False, num_workers=0)

        # sanity check begins here
        print('*******sanity check *********')
        for k, v in milnet.named_parameters():
            if v.requires_grad == True:
                print(k)

        # loss, optim, schduler
        if args.num_classes < 2:
            criterion = nn.BCEWithLogitsLoss()
        else:
            criterion = nn.CrossEntropyLoss()
        original_params = []
        confounder_parms = []
        for pname, p in milnet.named_parameters():
            if ('confounder' in pname):
                confounder_parms += [p]
                print('confounders:', pname)
            else:
                original_params += [p]
        optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, milnet.parameters()),
                                     lr=args.lr, betas=(0.5, 0.9),
                                     weight_decay=args.weight_decay)

        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.num_epochs, 0.000005)

        best_score = 0


        for epoch in range(1, args.num_epochs):
            start_time = time.time()
            train_loss_bag = train(train_loader, milnet, criterion, optimizer, args, log_path, epoch - 1, scaler)  # iterate all bags
            print('epoch time:{}'.format(time.time() - start_time))
            test_loss_bag, avg_score, aucs, thresholds_optimal = test(test_loader, milnet, criterion, optimizer, args,
                                                                      log_path, epoch)
            info = 'Epoch [%d/%d] train loss: %.4f test loss: %.4f, average score: %.4f, AUC: ' % (
            epoch, args.num_epochs, train_loss_bag, test_loss_bag, avg_score) + '|'.join(
                'class-{}>>{}'.format(*k) for k in enumerate(aucs)) + '\n'
            with open(log_path, 'a+') as log_txt:
                log_txt.write(info)
            print('\r Epoch [%d/%d] train loss: %.4f test loss: %.4f, average score: %.4f, AUC: ' %
                  (epoch, args.num_epochs, train_loss_bag, test_loss_bag, avg_score) + '|'.join(
                'class-{}>>{}'.format(*k) for k in enumerate(aucs)))

            scheduler.step()
            current_score = (sum(aucs) + avg_score) / 2
            if current_score >= best_score:
                best_score = current_score
                save_name = os.path.join(save_path, str(run + 1) + f'_{fold}.pth')
                torch.save(milnet.state_dict(), save_name)
                with open(log_path, 'a+') as log_txt:
                    info = 'Best model saved at: ' + save_name + '\n'
                    log_txt.write(info)
                    info = 'Best thresholds ===>>> ' + '|'.join(
                        'class-{}>>{}'.format(*k) for k in enumerate(thresholds_optimal)) + '\n'
                    log_txt.write(info)
                print('Best model saved at: ' + save_name)
                print(
                    'Best thresholds ===>>> ' + '|'.join('class-{}>>{}'.format(*k) for k in enumerate(thresholds_optimal)))
            if epoch == args.num_epochs - 1:
                save_name = os.path.join(save_path, f'_{fold}_last.pth')
                torch.save(milnet.state_dict(), save_name)
        log_txt.close()


if __name__ == '__main__':
    main()
