![멋사](likelion.png)
![대상](grandprize.png)
![짐빔](gymvymlogo.png)

***

![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-5.0.6-green?logo=django&logoColor=green)
![DRF](https://img.shields.io/badge/DRF-3.15.2-red)

***

NFC

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4%20Model%20B%20Rev%201.5p-red)
![RPi.GPIO](https://img.shields.io/badge/RPi.GPIO-0.7.0-yellow)
![MFRC522](https://img.shields.io/badge/mfrc522-1.6.0-blue)

***

deployment

![GCP](https://img.shields.io/badge/Google%20Cloud%20Platform-Cloud%20Run-blue)
![GCP](https://img.shields.io/badge/Google%20Cloud%20Platform-Cloud%20Build-red)
![gunicorn](https://img.shields.io/badge/gunicorn-22.0.0-green?logo=gunicorn&logoColor=white)
![PyYAML](https://img.shields.io/badge/PyYAML-6.0.1-green)

***

- **Raspberry Pi**: 저렴하고 강력한 싱글 보드 컴퓨터
- **RPi.GPIO**: Raspberry Pi의 GPIO 핀을 쉽게 제어할 수 있게 해주는 라이브러리
- **MFRC522**: RFID/NFC 리더 모듈을 다루기 위한 라이브러리로, 카드 인식 및 데이터 전송 기능을 제공

***

유저 dummy데이터 만드는 코드
```
import uuid
from django.utils import timezone
from account.models import CustomUser 
from django.utils.text import slugify
from faker import Faker

fake = Faker()

# 사용자 데이터 생성 함수
def create_custom_user(i):
    username = f'user_{i}'
    email = f'user_{i}@example.com'
    phone_number = fake.phone_number()
    address = fake.address()
    detail_address = fake.secondary_address()
    nickname = f'nickname_{i}'
    # user_image = 'static/default.png'
    birth = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
    usertype = fake.random_element(elements=(0, 1, 2))
    gender = fake.random_element(elements=('0', '1'))
    date_joined = timezone.now()
    last_login = timezone.now()

    user = CustomUser(
        user=uuid.uuid4(),
        nfc_uid=uuid.uuid4(),
        username=username,
        password='password',  # 실제로는 해시된 비밀번호를 사용해야 합니다.
        phone_number=phone_number,
        email=email,
        address=address,
        detail_address=detail_address,
        nickname=nickname,
        user_image=False,
        birth=birth,
        usertype=usertype,
        gender=gender,
        date_joined=date_joined,
        last_login=last_login
    )
    user.save()

# 30개의 사용자 데이터 생성
for i in range(1, 31):
    create_custom_user(i)

```
