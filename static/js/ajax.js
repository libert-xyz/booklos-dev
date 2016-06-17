$(document).ready(function(){


  $('#search').keyup(function() {
  //$('#search').typeahead({ source: function(query,process){


      $.ajax({

          type: "POST",
          url: "/search/",
          data:{

                'search_text': $('#search').val(),
               'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()

          },
          success: searchSuccess,
          dataType: 'html'

              });


          });

      });


function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data);

}
