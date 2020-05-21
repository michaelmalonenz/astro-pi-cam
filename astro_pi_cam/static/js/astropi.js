/* global $ */
function showPreview () {
  const selectFieldNames = ['resolution', 'iso', 'meter_mode', 'exposure_mode', 'shutter_speed']
  let queryParams = { 'num_shots': '1' }
  for (let field of selectFieldNames) {
    const value = $(`select[name="${field}"]`).children('option:selected').val()
    queryParams[field] = value
  }
  $.ajax({
    method: 'GET',
    url: `/camera/take_image`,
    data: queryParams
  }).done(function (data) {
    $('.modal #preview').attr('src', `data:image/jpeg;base64,${data}`)
    $('.modal').modal()
  })
}
