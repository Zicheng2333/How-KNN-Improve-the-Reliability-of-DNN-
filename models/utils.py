import torch
import torch.backends.cudnn as cudnn
import torchvision.models as models


def build_model(model_name):
    if model_name == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    elif model_name == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    elif model_name == "resnet101":
        model = models.resnet101(weights=models.ResNet101_Weights.IMAGENET1K_V1)
    else:
        raise ValueError("This models is not supported.")

    model = torch.nn.DataParallel(model)
    cudnn.benchmark = True
    model.eval()
    return model
