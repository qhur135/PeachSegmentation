## 복숭아 나무 영상에서 과실분할과 생장 모니터링을 위한 트랜스포머 모델     
### - 2022 KSC(Korea Software Congress) 일반논문    
https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11224200
### - 2022 JBNU 인공지능 경진대회   

swin transformer, yolact, mask r-cnn 코드 : https://github.com/open-mmlab/mmdetection   

* mmdetection 오픈소스로 실험 진행(용량문제로 학습 및 예측에 대한 코드는 mmdetection repository 참고)  
* 복숭아 dataset - peach_data 폴더  
* 복숭아 데이터에 알맞은 config 파일 작성 - config 폴더  
* 후처리 코드 기존 시각화 코드 수정하여 작성 - post_processing.py  

## 1. 서론
과실 인식 연구는 대부분 CNN 기반 모델을 활용하고 있으나 중복 예측이 발생하거나 추론 자원 및 시간 비용이 커서 현장 적용에 어려움이 있다.  
본 논문에서는 복숭아 사례 분할에 비전 트랜스포머 기반 모델을 적용하여 검출 정확도를 높이고 계산 소모 비용을 줄이고자 한다.

## 2. 데이터셋 구성
<img width="1000" alt="image" src="https://user-images.githubusercontent.com/67954861/209559925-94d74f7a-0111-42f4-bbb1-7a855c4fbbe0.png">  

- 국립원예특작과학원에서 수집된 데이터 이용     

- 총 126장     

- 데이터셋을 8:1:1로 분할하여 각각 Train, Validation, Test set으로 활용      


## 3. Swin-transformer 적용 및 실험
### * Instance Segmentation 성능 비교  

본 논문에서는 Swin-Transformer를 사용하여 복숭아 분할 실험을 진행하였으며, CNN기반 모델인 Mask R-CNN 및 YOLACT과 성능을 비교했다.   
성능 지표는 객체 분할에서 주로 쓰이는 AP (Average Precision)를 이용했다.   

<img width="500" alt="image" src="https://user-images.githubusercontent.com/67954861/209559032-e376f215-4000-4c29-9f28-ea2096ff7185.png">   

실험 결과, Swin-Transformer의 AP가 65.7%로 가장 높은 성능을 보여줬다. 특히, YOLACT와 26.0%의 큰 차이를 보였으며, IOU=0.5에서 Mask R-CNN과 6.30%의 의미 있는 차이를 보였다. 다만, IOU=0.75에서는 Mask R-CNN이 가장 높은 성능을 냈다.


### * 작은 객체에 대한 비교
<img width="500" alt="image" src="https://user-images.githubusercontent.com/67954861/209559096-3ddcfe29-393f-4465-a1c2-413e9c61df7c.png">
Swin-Transformer는 표가 보여주는 바와 같이 작은 물체 검출에 강건하다. 때문에 멀리 있거나 나뭇잎에 가려진 복숭아 검출에 유리하다. 

<img width="1500" alt="image" src="https://user-images.githubusercontent.com/67954861/209560129-1edd86da-d06a-4718-a1b1-e0564b6f33f6.png">  

노란색 박스는 복숭아가 나뭇잎에 가려진 경우이다. mask R-CNN은 나뭇잎에 가려진 경우에 복숭아를 검출해내지 못하지만, swin transformer는 나뭇잎에 가려진 작은 객체도 검출해낸다.
빨간색 박스는 복숭아가 멀리 있어 객체가 아주 작은 경우이다. mask R-CNN과 yolact는 아주 작은 객체를 검출해내지 못하지만, swin transformer는 멀리있는 작은 객체도 검출해낸다.

## 4. 생장 모니터링을 위한 후처리
### * 과실 크기 추정
분할된 복숭아 마스크에서 |𝑥_𝑚𝑎𝑥− 𝑥_𝑚𝑖𝑛|, |𝑦_𝑚𝑎𝑥− 𝑦_𝑚𝑖𝑛|로 각각 과폭과 과장을 구한다. 현재 구해진 과장, 과폭의 단위는 픽셀이지만, 향후 촬영 거리 등을 이용해 실 좌표계에서의 길이를 구할 수 있다.   

### * 과실 숙도 추정
향후 복숭아의 숙도를 예측하기 위해 복숭아 영역의 평균 색도를 측정한다. RGB 컬러모델은 빛의 영향을 많이 받는다. 때문에, 정확한 숙도 예측을 위해 휘도와 색 채널이 분리된 LAB 컬러 모델로 영상을 변환하고 적녹 색도를 표현하는 a* 채널 값을 이용했다.       
<img width="1000" alt="image" src="https://user-images.githubusercontent.com/67954861/209560196-55f38bdd-0a9f-4baa-bb65-6f69b162ed0c.png">    

LAB 컬러 모델로 변환 후 영역 별로 a* 채널의 평균을 구했을 때, 그림3은 영상에 포함된 복숭아 마스크의 a* 평균이 최소인 영상이고 그림 4는  최대인 영상이다. a* 채널 값이 높을수록 복숭아가 숙도가 높음을 예상할 수 있다. 향후 a*값을 과실의 숙도 예측 지표로 활용하기에 충분하다.   

## 5. 결론 및 고찰  
복숭아 생장 모니터링을 위해서는 무엇보다 정확한 과실 객체 분할이 중요하다. Swin-transformer는 속도와 성능 면에서 복숭아 생장 예측 모델에 적합하다. Swin-transformer는 추론에 영상 당 약 0.07초가 소요되었으며, Mask R-CNN은 영상 당 약 0.15초가 소요되었다.     
AP@0.5에서 Swin-transformer는 91.9% 성능을 냈으며, Mask R-CNN은 85.6%를 달성했다. 작은 객체에 대해서는 AP@0.5:0.95에서 Swin-transformer는 60.0%, Mask R-CNN은 46.1%를 보였다.
향후 중심점 추적 모델(Centroid tracking) 등을  이용하여 동영상에서의 복숭아 개수도 카운팅 할 예정이다. 또한, 로봇에 알고리즘을 적용하여 실제 복숭아 생장 모니터링 로봇을 개발하고자 한다.    

## 6. 사사
본 연구는 2022년 과학기술정보통신부 및 정보통신기획평가원의 SW중심대학지원사업(2022-0-01067), 과학기술정보통신부 여대학원생 공학연구팀제 지원사업(WISET-2022-126호) 및 농촌진흥청 연구 사업(과제번호: PJ0156462022)의 연구결과로 수행되었음  






