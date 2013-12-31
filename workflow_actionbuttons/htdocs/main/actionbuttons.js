jQuery(document).ready(function($) {
    var inlinebuttons = $("<div>").attr("id", "actionbuttons");
    for( var i=0; i<WorkflowActionButtonsPlugin.action_buttons.length; ++i ) {
        var button = WorkflowActionButtonsPlugin.action_buttons[i];
        $(button).appendTo(inlinebuttons);
    }
    inlinebuttons.insertBefore(".trac-topnav");

    inlinebuttons.on("click", "[name=act]", function(evt) {

        var action = $(this).siblings("[name=action]").val(),
            commentBefore = ($(this).data("comment") === "required" ) || evt.altKey,
            supplemental = $(this).closest("label").find(".supplemental");
        if( supplemental.length ) {
            var container = $("<form>").html(supplemental.html());
            container.on("submit", function() {
                var data = { action: action };
                $(this).find(":input").each(function() {
                    if( $(this).attr("name") ) {
                        data[$(this).attr("name")] = $(this).val();
                    }
                });
                actOnTicket(data);
                $.modal.close();
                return false;
            });
            container.appendTo("body").modal();
            window.setTimeout(function() { $(container).find(":input:first").focus() }, 0);
            return false;
        }
    if( commentBefore ) {
        var container = $("<div>").html("<form><textarea style='width:95%' rows='5' name='comment' placeholder='Enter your comment'></textarea><input type='submit' style='margin-left: 90%' value='Go' /></form>");
        
        container.find("form").on("submit", function() {

            actOnTicket({ action: action,
                          comment: container.find("form [name=comment]").val() });
            $.modal.close();
            return false;
        });
        container.appendTo("body").modal();
        window.setTimeout(function() { container.find("form [name=comment]").focus(); }, 0);
        return false;
    } else {
      actOnTicket({ action: action });
    }

    });

    function actOnTicket(data) {
        var form = $("#propertyform");
        $.each(data, function(key, val) {
            var input = form.find(":input[name="+key+"]");
            if( input.attr("type") == "radio" ) {
                input.filter("[value="+val+"]").prop("checked", true);
            } else {
                input.val(val);
            }
        });
        $(form).find("input[type=submit][name=submit]").click();
    };
});

