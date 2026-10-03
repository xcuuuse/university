function check(questionsCount) {
    for (var i = 1; i <= questionsCount; ++i) {
        for (var j = 0; j <= 5; ++j) {
            var element = '#form1 #' + i + j;
            if ($(element)) {
                $(element).closest('label').css("background", "");
            }
        }
    }
    $('#form1 #answers').html("");
    $('#form1 #answers').css("background", "")

    var errorsCount = 0;
    for (var i = 1; i <= questionsCount; ++i) {
        var element = '#form1 #' + i + answers[i - 1];
        if ($(element).prop('checked')) {
            $(element).closest('label').css("background", "#00cc33");
        } else {
            ++errorsCount;
            for (var t = 0; t <= 5; ++t) {
                var selected = '#form1 #' + i + t;
                if ($(selected) && $(selected).prop('checked')) {
                    $(selected).closest('label').css("background", "red");
                    break;
                }
            }
        }
    }
    var correctAnswersCount = questionsCount - errorsCount;
    if ($('#form1 #answers') && correctAnswersCount == questionsCount) {
        $('#form1 #answers').html("all right!");
        $('#form1 #answers').css("background", "#00cc33")
    } else if ($('#form1 #answers')) {
        $('#form1 #answers').html("mistakes: " + errorsCount + " of " + questionsCount);
        $('#form1 #answers').css("background", "red")
    }

    window.scroll(0, 0);
}