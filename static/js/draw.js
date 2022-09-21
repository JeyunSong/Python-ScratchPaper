// 캔버스 설정
const canvas = document.getElementById("canvas");
canvas.width = 600;
canvas.height = 600;

let context = canvas.getContext("2d");
let start_background_color = "ghostwhite";
context.fillStyle = start_background_color;
context.fillRect(0, 0, canvas.width, canvas.height);

// 펜설정, 컬러 굵기
let draw_color = "black";
let draw_width = "2";
let is_drawing = false;

// 이전으로 돌리기 // 빈배열을 만든다.
let restore_array = [];
let index = -1;

// 컬러변경
function change_color(element) {
    draw_color = element.style.background;
}

canvas.addEventListener("touchstart", start, false);
canvas.addEventListener("touchmove", draw, false);
canvas.addEventListener("mousedown", start, false);
canvas.addEventListener("mousemove", draw, false);

canvas.addEventListener("touchend", stop, false);
canvas.addEventListener("mouseup", stop, false);
canvas.addEventListener("mouseout", stop, false);


// 이미지 그리는 부분
function start(event) {
    is_drawing = true;
    context.beginPath();
    context.moveTo(event.clientX - canvas.offsetLeft,
        event.clientY - canvas.offsetTop);
    event.preventDefault();

    // 이전것 저장해두기 // 이벤트가 마우스아웃이 아닐때 마우스가 안에 있을때 위치값 저장.
    if (event.type != 'mouseout') {
        restore_array.push(context.getImageData(0, 0, canvas.width, canvas.height));
        index += 1;
    }
    console.log(restore_array);
}

function draw(event) {
    if (is_drawing) {
        context.lineTo(event.clientX - canvas.offsetLeft,
            event.clientY - canvas.offsetTop);
        context.strokeStyle = draw_color;
        context.lineWidth = draw_width;
        context.lineCap = "round";
        context.lineJoin = "round";
        context.stroke();
    }
}

function stop(event) {
    if (is_drawing) {
        context.stroke();
        context.closePath();
        is_drawing = false;
    }
    event.preventDefault();
}


// 지우기
function clear_canvas() {
    context.fillStyle = start_background_color;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillRect(0, 0, canvas.width, canvas.height);

    restore_array = [];
    index = -1;
}

// 뒤로가기
function undo_last() {
    if (index <= 0) {
        clear_canvas();
    } else {
        index -= 1;
        restore_array.pop();
        context.putImageData(restore_array[index], 0, 0);
    }
}


// 저장하기
function save() {
    canvas.toBlob((blob) => {

        const a = document.createElement('a');
        document.body.append(a);
        a.download = 'export{timestamp}.png';
        a.href = URL.createObjectURL(blob);
        a.click();
        a.remove();
    });
}


function posting() {
    const canvas = document.getElementById('canvas');
    const dataURL = canvas.toDataURL();
    canvas.toDataURL('image/jpeg', 0.5);

    let title = $('#title').val()
    let text = $('#text').val()
    let like_count = 0

    $.ajax({
        type: 'post',
        url: '/save_post',
        data: {picture: dataURL, title: title, text: text, like_count: like_count},
        success: function (response) {
            alert(response)
            window.location.replace('/')
        }
    })
}

function send_post(num) {

    // window.location.replace('/post/user')

    let postnum = String(num)
    console.log(typeof(postnum))
    console.log(postnum)

    window.location.href='/user/'+postnum
}









