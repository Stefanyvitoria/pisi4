function postFile() {
    let file = document.querySelector("#file").files;
    console.log(file)
    
    const data = { file: file };

    fetch("http://127.0.0.1:5000/teste", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    })
    .then((response) => console.log(response))
    // $.post('http://127.0.0.1:5000/teste', {
    //     file : file
    // }, function(response) {
    //     console.log(response);
    // });
    // console.log(file)

}


// function handleFiles(fileup) {
//     $.post('teste', {
//         file : fileup
//     }, function(response) {
//         console.log(response);
//     });
// }
