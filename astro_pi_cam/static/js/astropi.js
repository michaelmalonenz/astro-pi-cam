/* global $ */
function showPreview () {
  const fieldNames = ['resolution', 'iso', 'meter_mode', 'exposure_mode', 'shutter_speed']
  let queryParams = []
  for (let field of fieldNames) {
    const value = $(`select[name="${field}]`).children('option:selected').val()
    queryParams.push(`${field}=${value}`)
  }
  $.ajax({
    method: 'POST',
    url: `/camera/take_image?${queryParams.join('&')}`
  }).done(function (data) {
    $('.modal #preview').attr('src', `data:image/jpeg;base64,${data}`)
    $('.modal').modal()
  })
}
