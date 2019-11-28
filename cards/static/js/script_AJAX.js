$('img.chosen').click(function(){
<!--    select and unselect-->
    if ($(this).data('action') == 'unselected') {
        $(this).css({border: "10px solid red"})
        $(this).data('action', 'selected')
        console.log($(this).data('action'))
    } else {
        $(this).css({border: "0px solid red"})
        $(this).data('action', 'unselected')
    }
    console.log($(this).attr('src'))
    $.post('{% url "cards:meal_image" %}',
    {src: $(this).attr('src')},
        function(data){
            if (data['status'] == 'ok'){
                var url = $('img.chosen').src
                console.log(url)
                }
            }
        );
});