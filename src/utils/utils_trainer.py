import os
from datetime import datetime

import torch


def manual_seed(random_seed, device):
        """
        Set the environment for reproducibility purposes.
        Args:
            config (defaultdict): set of parameters
                usage of:
                    random seed (int):
                    device (torch.device):
        """
        import random
        import numpy as np
        random.seed(random_seed)
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)
        if 'cuda' in device.type:
            torch.cuda.empty_cache()
            torch.cuda.manual_seed_all(random_seed)


def adjust_evaluators(d1, dd2, denom, scope, phase):
    '''
    Adoptuje evaluatory z dd2 do d1.
    Jeżeli klucz kończy się phase (train/valid/test), to sprawdza czy istnieje scope (running/epoch) by upewnić się że doda go właściwie.
    Jeżeli klucz nie jest podzielony przez "/" to dodaje scope i phase.
    W przeciwnym przypadku dodaje scope, sprawdzając czy istnieje scope by upewnić się że doda go właściwie.
    '''
    for evaluator_key in dd2:
        eval_key = str(evaluator_key).split('/')
        if 'train' in evaluator_key or 'valid' in evaluator_key or 'test' in evaluator_key:
            eval_key = '/'.join(eval_key[:-1]).split('_')
            eval_key = '_'.join(eval_key[1:]) if eval_key[0] in {'running', 'epoch'} else '_'.join(eval_key)
            d1[f'{scope}_{eval_key}/{phase}'] += dd2[evaluator_key] * denom
        elif len(eval_key) == 1:
            d1[f'{scope}_{eval_key[0]}/{phase}'] += dd2[evaluator_key] * denom
        else:
            eval_key = '/'.join(eval_key).split('_')
            eval_key = '_'.join(eval_key[1:]) if eval_key[0] in {'running', 'epoch'} else '_'.join(eval_key)
            d1[f'{scope}_{eval_key}'] += dd2[evaluator_key] * denom
    return d1


def adjust_evaluators_pre_log(d1, denom, round_at=4):
    d2 = {}
    for k in d1:
        d2[k] = round(d1[k] / denom, round_at)
    return d2


def update_tensor(a, b):
    c = torch.cat([a, b])
    return c


def load_model(model, path):
    model.load_state_dict(torch.load(path))
    return model


def save_model(model, path):
    torch.save(model.state_dict(), path)


def create_paths(base_path, exp_name):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_path = os.path.join(os.getcwd(), f'{base_path}/{exp_name}/{date}')
    save_path_base = f'{base_path}/checkpoints'
    os.makedirs(save_path_base)
    save_path = lambda step: f'{save_path_base}/model_step_{step}.pth'
    return base_path, save_path


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self



