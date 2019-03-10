const container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
const options = { //지도를 생성할 때 필요한 기본 옵션
  center: new daum.maps.LatLng(37.5839, 127.0588),
  level: 3 //지도의 레벨(확대, 축소 정도)
};

const map = new daum.maps.Map(container, options); //지도 생성 및 객체 리턴

// https://stackoverflow.com/questions/298772/django-template-variables-and-javascript
const pos=JSON.parse(pos_string)
// console.log(JSON.parse(pos_string))

const circle=pos.map((e,i)=>{
  return new daum.maps.Circle({
      center : new daum.maps.LatLng(e.x, e.y),  // 원의 중심좌표 입니다
      radius: 20, // 미터 단위의 원의 반지름입니다
      strokeWeight: 2, // 선의 두께입니다
      strokeColor: '#75B8FA', // 선의 색깔입니다
      strokeOpacity: 0.3, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
      strokeStyle: 'dashed', // 선의 스타일 입니다
      fillColor: '#F1685E', // 채우기 색깔입니다
      fillOpacity: 0.3  // 채우기 불투명도 입니다
  });
  // 지도에 원을 표시합니다
});
showCircles(circle);
// circle.map(e=>e.setMap(map)) //다 뿌리기
// http://apis.map.daum.net/web/sample/drawShape 참고

//click event
daum.maps.event.addListener(map, 'click', function(mouseEvent) {
    addMarker(mouseEvent.latLng);
});

// 마커를 생성하고 지도위에 표시하는 함수입니다
var markers=[];
function addMarker(position) {
    // 마커를 생성합니다
    var marker = new daum.maps.Marker({
        position: position
    });
    console.log(position['ib'],position['jb'])
    // 마커가 지도 위에 표시되도록 설정합니다
    marker.setMap(map);

    // 생성된 마커를 배열에 추가합니다
    markers.push(marker);
}

// 배열에 추가된 마커들을 지도에 표시하거나 삭제하는 함수입니다
function setMarkers(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function showCircles(circle){
  for(let i=0;i<circle.length;i++){
    circle[i].setMap(map);
  }
}
