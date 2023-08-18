from maskgan.model import MaskGAN
from msg_id_dictionary import MSGIDDictionary
from maskgan.mask import StochasticMask
from maskgan.dataset import MSGIDSequence

import util_config
import data_preparation

import torch
import numpy as np

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def run_maskgan() -> None:
    param_config = util_config.get_param_config()
    label_info_list = param_config['label_info_list']

    train_data, train_label, _, _, _, _, _ \
        = data_preparation.load_data(128, label_info_list, 'before_aug', '', -1)

    filtered_train_data = [train_data[(train_label == 0) | (train_label == 1)]]
    filtered_train_label = [train_label[(train_label == 0) | (train_label == 1)]]

    ping_data = train_data[train_label == 2]
    ping_label = train_label[train_label == 2]
    perm = np.random.permutation(ping_data.shape[0])
    ping_data = ping_data[perm][:2000]
    ping_label = ping_label[perm][:2000]
    filtered_train_data.append(ping_data)
    filtered_train_label.append(ping_label)

    request_data = train_data[train_label == 3]
    request_label = train_label[train_label == 3]
    perm = np.random.permutation(request_data.shape[0])
    request_data = request_data[perm][:2000]
    request_label = request_label[perm][:2000]
    filtered_train_data.append(request_data)
    filtered_train_label.append(request_label)

    train_data = np.vstack(filtered_train_data)
    train_label = np.hstack(filtered_train_label)

    print(f'Train Data Info.')
    print(f'Attack-free: {(train_label == 0).sum()}')
    print(f'Heartbeat: {(train_label == 1).sum()}')
    print(f'Ping: {(train_label == 2).sum()}')
    print(f'Request: {(train_label == 3).sum()}')

    one_hot_label_list = []
    for label in train_label:
        one_hot_label = np.zeros(len(label_info_list))
        one_hot_label[int(label)] = 1.0
        one_hot_label_list.append(one_hot_label)
    train_label = np.vstack(one_hot_label_list)

    msg_id_dict = MSGIDDictionary()
    masker = StochasticMask(0.3)
    msg_id_sequence = MSGIDSequence(train_data, train_label, masker, msg_id_dict, DEVICE)

    batch_size = 512
    gen_hidden_size = 64
    dis_hidden_size = 64
    gen_lr = 0.0001
    dis_lr = 0.005
    seq_len = 128
    gen_pre_epochs = 1
    dis_pre_epochs = 1
    adv_epochs = 1
    n_vocabs = msg_id_dict.get_n_vocabs()

    save_path = ''
    train_dataset = msg_id_sequence

    # Model build
    mask_gan = MaskGAN(train_dataset, len(label_info_list), n_vocabs, batch_size, gen_hidden_size, dis_hidden_size,
                       gen_lr, dis_lr, seq_len, save_path, DEVICE)

    # Train
    mask_gan.train(gen_pre_epochs, dis_pre_epochs, adv_epochs)

    # Eval
    return


if __name__ == '__main__':
    run_maskgan()
