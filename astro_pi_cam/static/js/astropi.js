function showPreview () {

    $.ajax({
        method: 'POST',
        url: '/camera/take_image'
    }).done(function (data) {
        $('.modal #preview').attr('src', `data:image/jpeg;base64,${data}`)
        $('.modal').modal()
    })
}
