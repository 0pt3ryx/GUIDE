import torch
from torch.utils.data import Dataset
import numpy as np

"""
class MSGIDSequence(Dataset):
    def __init__(self, data_arr: np.ndarray, label_arr: np.ndarray,
                 mask_builder, can_id_dict, device: torch.device):
        self.sequences = data_arr
        self.labels = label_arr
        assert self.sequences.shape[0] == self.labels.shape[0]
        self.mask_builder = mask_builder
        self.can_id_dict = can_id_dict
        self.device = device

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx) -> tuple:
        return self.sequences[idx], self.labels[idx]
"""


class MSGIDSequence(Dataset):
    def __init__(self, data_arr: np.ndarray, device: torch.device):
        self.sequences = data_arr
        self.device = device

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return torch.Tensor(self.sequences[idx]).type(torch.LongTensor).to(self.device), \
               torch.Tensor([1]).type(torch.LongTensor).to(self.device)
