## hostname 변경

- 해당 파일에 들어가서 각각 server1, server2, server3로 변경해주기 
```
sudo vi /etc/hostname
sudo reboot
```

## ssh 연결

#### key 생성 및 연결 
- 각자 서버에서 인증 key 생성 
```
# 명령어 입력 후 enter 3번 작성
ssh-keygen -t rsa
```

- 모든 서버의 pub키를 각 서버의 authorized_keys에 등록해주기 
```
cat id_rsa.pub
vi authorized_keys

----
# 각 서버의 pub 키를 등록해주기 
```

#### config 파일 설정
- username부분은 따로 수정해야함
```
Host server1
  HostName server1
  User username
  IdentityFile ~/.ssh/id_rsa

Host server2
  HostName server2
  User username
  IdentityFile ~/.ssh/id_rsa

Host server3
  HostName server3
  User username
  IdentityFile ~/.ssh/id_rsa
```
