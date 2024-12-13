# ATMProject (prototype)
---------
ATM 기기에서 사용자 카드와 PIN번호를 통해 인증. 인증 통과 시 계좌정보 조회, 입금, 출금 수행.
(은행 API 연동 및 ATM 기기의 현찰 조회 기능 미구현)

---------
### 주요기능
* Main
  * 사용자 카드와 PIN번호 인증
    * 개인정보 저장 X
  * 인증성공 토큰을 토대로 사용자 요청 수행 (계좌정보 조회, 입금, 출금)
    * [prototype] 계좌정보 조회는 미구현
    * 입금, 출금 시 ATM Device의 현찰 금액 갱신
      * ATM Device의 현찰보다 많은 출금 시도 방지
* ATM Deivce
  * ATM Deivce 정보 조회
  * [prototype] ATM Deivce 등록
  * [prototype] ATM Deivce 현찰 금액 갱신
* Bank
  * [prototype] Bank 정보 조회
  * [prototype] Bank 등록

### API Endpoint
* Main
  * GET /atm/info/<atm_deivce_id>/
    * 해당 ATM Device의 정보 조회      
  * POST /atm/validate/
    * 사용자 카드와 PIN번호 인증
      * Params:
        * card_number
        * pin
    * 입력받은 PIN번호를 sha-256으로 암호화 후, 은행으로부터 받은 값과 비교
      * 은행에서 평문이 아닌, sha-256 암호화 값을 준다고 가정
    * 인증 성공 시 30초 수명의 토큰 리턴
  * POST /atm/activity/
    * 위 토큰을 토대로 사용자 요청 수행 (계좌정보 조회, 입금, 출금)
      * Params:
        * card_number
        * token
        * activity_type
        * atm_deivce_id
    * 토큰과 카드 번호 조합 체크
      * 토큰 수명 체크 -> 요청 수행 후 토큰 삭제
    * ATMActivityHistory 로그 기록
* ATM Device
  * GET /atm_device/get_atm_device_id/
    * ATM Device 정보 조회 (남은 현찰 금액 포함)
      * Params:
        * atm_device_id
    * cache 활용
  * [prototype] POST /atm_deivce/create/
    * ATM Device 등록
* Bank
  * [prototype] GET /bank/get/<bank_code>/
    * cache 활용
  * [prototype] POST /bank/add/

### Setup
```
pip install requirements.txt
```

### Testing
```
python manage.py test atm_reading_proj.main.tests.ATMTestCase
```
