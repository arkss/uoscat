##  uos cat



* 기능
  * 소셜로그인
  * 포스팅
  * 이름 투표
  * 밥 준 횟수 및 시간
* app
  * 소셜 로그인 loginapp
    * templates
      * sign up
      * sign in
  * 나머지 기능들 
    * templates
      * home -> 고양이 사진들
      * create -> 새로운 고양이 등록(사진, 이름, 성별, 주 서식지, 기타 상세설명)
      * detail -> 각 포스팅의 상세페이지 , 이름 투표 기능, 마지막으로 밥 준시간
    * views
      * home
      * create
      * detail
      * vote
      * feed
    * models
      * cat(각 고양이들의 데이터)
        * name
        * image
        * gender
        * habitat(위도 경도 좌표)
        * body(상세설명)
        * lasteat(마지막으로 밥 준 시간)
      * vote
        * title
        * onetoonefiled(cat이랑 대응)
      * choice
        * forigenkey 를 vote에 줌 -> 이러면 vote에 여러가지 선택지가 생길 수 있음
        * name(고양이 이름)
        * count(투표 수)
* 추가적인 기능들
  * 댓글쓰기 및 삭제 및 수정
  * 글 삭제 및 수정
  * 



