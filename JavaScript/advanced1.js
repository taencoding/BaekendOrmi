// 전체 product의 갯수와
// 전체 가격의 평균을 구해주세요.

// fetch('http://test.api.weniv.co.kr/mall')
//     .then(data => data.json())
//     .then(data => console.log(data))


fetch('http://test.api.weniv.co.kr/mall')
    .then(data => data.json())
    .then(data => {
        sum = 0
        for (const i of data) {
            sum += i.price
        }
        count = data.length
        avg = sum / count
        console.log(count)
        console.log(avg)
    })