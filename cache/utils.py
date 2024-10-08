import os
import torch
import numpy as np
import torch.nn as nn
from torchvision import transforms, models

from .EmbeddingWrapper import EmbeddingWrapper
from models.utils import build_model


class Bottom(nn.Module):
    def __init__(self, original_model):
        super(Bottom, self).__init__()
        self.features = nn.Sequential(*list(original_model.children())[:-1])

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return x


class TopNoSoftmax(nn.Module):
    def __init__(self, original_model):
        super(TopNoSoftmax, self).__init__()
        self.features = nn.Sequential(*[list(original_model.children())[-1]])

    def forward(self, x):
        x = self.features(x)
        return x


def build_classifier(cfg):
    model_name = cfg.MODEL.ARCH

    model = build_model(cfg)
    model_bottom, model_top = Bottom(model), TopNoSoftmax(model)
    extractor = EmbeddingWrapper(model_bottom, model, model_name)
    extractor.model_name = model_name

    return extractor
