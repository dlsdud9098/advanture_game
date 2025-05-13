# 시작
파이썬의 문법을 어느정도 익혔으니, 이제 파이썬으로 게임을 만들어 보려고 한다.

나중에 gui를 만들고 ai도 넣어보려고 한다.

# 생각나는 작업 목록 (0501)
- [ ] 게임 전체적인 부분 <span style="opacity: 0.3;">(0501)</span>
  - [x] 캐릭터 생성시 닉네임 중복 확인 <span style="opacity: 0.3;">(0501)</span>
  - [x] 캐릭터 생성시 데이터 저장하기 <span style="opacity: 0.3;">(0501)</span>
  - [x] 캐릭터 로드하기 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 난이도 설정 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 데이터 삭제 <span style="opacity: 0.3;">(0502)</span>
- [ ] 캐릭터 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 직업 만들기 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 직업별 스텟 조정하기 (0501) <span style="opacity: 0.3;">(0501)</span>
  - [ ] 직업별 스킬 만들기 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 상태창 표시하기 <span style="opacity: 0.3;">(0501)</span>
- [ ] 스킬 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 스킬에 조건 걸기 <span style="opacity: 0.3;">(0501)</span>
- [ ] 아이템 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 아이템에 조건 걸기 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 아이템 드랍 확률 넣기 <span style="opacity: 0.3;">(0501)</span>
- [ ] 몬스터 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 몬스터 구상하기 <span style="opacity: 0.3;">(0501)</span>
  - [ ] 몬스터별 드랍템 넣기 <span style="opacity: 0.3;">(0501)</span>
- [ ] NPC <span style="opacity: 0.3;">(0501)</span>
  - [ ] 상인 만들기 <span style="opacity: 0.3;">(0501)</span>
- [ ] GUI <span style="opacity: 0.3;">(0501)</span>
- [ ] AI <span style="opacity: 0.3;">(0501)</span>

# 목표
- 텍스트 기반으로 RPG 게임 완성하기
- GUI 만들기
- AI 사용하기

# 파일
https://github.com/dlsdud9098/advanture_game

# 구조
├── README.md  
├── develop_logs  
│   └── 0501 logs 01.md  
├── display  
│   ├── __pycache__  
│   │   └── display_select.cpython-311.pyc  
│   └── display_select.py  
├── main.py  
├── pyproject.toml  
├── saves  
│   ├── __pycache__  
│   │   └── save_loads.cpython-311.pyc  
│   ├── datas  
│   │   └── saves.json  
│   └── save_loads.py  
├── temp.ipynb  
├── unit  
│   ├── __pycache__  
│   │   ├── create_character.cpython-311.pyc  
│   │   └── player.cpython-311.pyc  
│   ├── character_class  
│   │   ├── __pycache__  
│   │   │   └── warrior.cpython-311.pyc  
│   │   ├── character_settings.md  
│   │   └── warrior.py  
│   ├── create_character.py  
│   ├── item.py  
│   ├── monster.py  
│   └── player.py  
└── uv.lock  