/* Javascript for SelfCheckXBlock. */
function SelfCheckXBlock(runtime, element) {

    function post_submit(result) {
	$('.solution',element).show();
	$('.submit',element).text("resubmit");
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'student_submit');

    $('.submit', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"input": $(".input",element).val() }),
            success: post_submit
        });
    });
}
