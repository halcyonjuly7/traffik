$("#submit").click(function() {
  $.ajax({
    method: "GET",
    url: "http://45.55.198.11:7777/nearest",
    data: {"zip_codes": $("input").val()},
    success: function(data) {
      console.log(data);
    }
  })
})