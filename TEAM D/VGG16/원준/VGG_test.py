import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision.datasets as datasets


import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from VGG_model import VGG
import torch
import torch.nn as nn
from tqdm import trange


learning_rate = 0.001

# CUDA 사용 여부 확인 후 디바이스 설정
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# VGG 모델 인스턴스화 및 디바이스로 이동
model = VGG(base_dim=64).to(device) # 첫 번째 컨볼루션 레이어가 출력하는 채널 수가 64



# 데이터 변환
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# 테스트 데이터셋 로드 (CIFAR-10 예제)
test_dataset = datasets.CIFAR10(root='./data', train=False, transform=transform, download=True)

# DataLoader 생성
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 모델 평가
correct = 0
total = 0

model.eval()

# 인퍼런스 모드를 위해 no_grad
with torch.no_grad():  # 학습 x 
    # 테스트로더에서 이미지와 정답 불러오기 
    for image, label in test_loader:
    
        x = image.to(device)
        y = label.to(device)

        output = model.forward(x)
        _, output_index = torch.max(output, 1) # 가장 큰 값 인덱스만 선택

        # total은  최종 10,000 
        total += label.size(0)
        correct += (output_index == y).sum().float()  #정답 클래스의 인덱스 y와 얼마나 일치하는지지

    # 정확도 도출
    print("Accuracy of Test Data: {:.2f}%".format(100 * correct / total))