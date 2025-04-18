import torch
import torch.nn as nn

architecture_config = [
    # (kernel size, # filters, stride, padding)
    (7, 64, 2, 3),
    "M", # max pooling
    (3, 192, 1, 1),
    "M",
    (1, 128, 1, 0),
    (3, 256, 1, 1),
    (1, 256, 1, 0),
    (3, 512, 1, 1),
    "M",
    (1, 256, 1, 0), (3, 512, 1, 1),
    (1, 256, 1, 0), (3, 512, 1, 1),
    (1, 256, 1, 0), (3, 512, 1, 1),
    (1, 256, 1, 0), (3, 512, 1, 1),
    (1, 512, 1, 0),
    (3, 1024, 1, 1),
    "M",
    (1, 512, 1, 0), (3, 1024, 1, 1),
    (1, 512, 1, 0), (3, 1024, 1, 1),
    (3, 1024, 1, 1),
    (3, 1024, 2, 1),
    (3, 1024, 1, 1),
    (3, 1024, 1, 1)
]

class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)
    
    def forward(self, x):
        return self.leakyrelu(self.batchnorm(self.conv(x)))
    
class Yolov1(nn.Module):
    def __init__(self, in_channels=3, **kwargs):
        super(Yolov1, self).__init__()
        self.architecture = architecture_config
        self.in_channels = in_channels
        self.darknet = self._create_conv_layers(self.architecture)
        self.fcs = self._create_fcs(**kwargs)
    
    def forward(self, x):
        x = self.darknet(x)
        return self.fcs(torch.flatten(x, start_dim=1))
    
    def _create_conv_layers(self, architecture):
        layers = []
        in_channels = self.in_channels

        for x in architecture:
            if type(x) == tuple:
                layers += [CNNBlock(
                    in_channels,
                    x[1],
                    kernel_size=x[0],
                    stride=x[2],
                    padding=x[3]
                )]
                in_channels = x[1]
            elif type(x) == str:
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            
        return nn.Sequential(*layers)
        
    def _create_fcs(self, split_size, num_boxes, num_classes):
        S, B, C = split_size, num_boxes, num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024*S*S, 496), # should be 4096
            nn.Dropout(0.5),
            nn.LeakyReLU(0.1),
            nn.Linear(496, S*S*(C+B*5))
        )

