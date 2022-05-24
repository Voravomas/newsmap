export function dateToTimestamp(inputDate) {
    let normalDate = inputDate;
    console.log(normalDate)
    normalDate = normalDate.split("-")
    var newDate = new Date( normalDate[0], normalDate[1] - 1, normalDate[2]);
    return newDate.getTime() / 1000;
}

export function timestampToDate(UNIX_timestamp){
    var a = new Date(UNIX_timestamp * 1000);
    var year = a.getFullYear();
    var month = a.getMonth() + 1;
    var date = a.getDate();
    var dateZero = date < 10 ? '0' : '';
    var monthZero = month < 10 ? '0' : '';
    return year + '-' + monthZero + month + '-' + dateZero + date;
}