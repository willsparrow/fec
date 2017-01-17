/**
 * Created by wangpenglong801 on 2016-04-05.
 */
$(document).ready(function(){
    $(".btn-add-to-cart").click(function(){
        prod_id = ($(this).parent().parent().children("div.prod-qty").children("input#id_prod_id").val());
        qty = ($(this).parent().parent().children("div.prod-qty").children("input#id_qty").val());
        // 重置商品数量为1
        $(this).parent().parent().children("div.prod-qty").children("input#id_qty").val(1);
        console.log(qty)
        $.post("/ec/add_to_cart/", {'prod_id':prod_id, 'qty':qty}, function(ret){
            //console.log(ret)
            $("#msg-add-to-cart").html(ret);
            $("#modal-add-to-cart").modal('show');
       });
    });

    $(".icon-add").click(function () {
        prod_id = $(this).parent().children("input#id_prod_id").val();
        // $(this).parent().children("input#id_prod_qty").val(parseInt($(this).parent().children("input#id_prod_qty").val()) + 1);
        console.log($(this).parent().children("input#id_prod_qty").val());
        console.log(prod_id);
        qty = 1;
        $.post("/ec/add_prod/", {'prod_id':prod_id, 'qty':qty}, function(ret){
            // console.log(ret)
            // $("#block_cart").html(ret);
            location.reload();
       });

    })

    $(".icon-del").click(function () {
        prod_id = $(this).parent().children("input#id_prod_id").val();
        // $(this).parent().children("input#id_prod_qty").val(parseInt($(this).parent().children("input#id_prod_qty").val()) + 1);
        console.log($(this).parent().children("input#id_prod_qty").val());
        console.log(prod_id);
        qty = parseInt($(this).parent().children("input#id_prod_qty").val());
        if (qty == 1){
            console.log($(this).attr("class"));
            //$(this).attr("class", "disabled");
            $(this).attr("disabled",true);
            console.log($(this).attr("class"));
        }
        else{
            qty = 1;
            $.post("/ec/del_prod/", {'prod_id':prod_id, 'qty':qty}, function(ret){
                // console.log(ret)
                // $("#block_cart").html(ret);
                location.reload();
           });
        }

    })

    $(".icon-rmv").click(function () {
        prod_id = $(this).parent().children("input#id_prod_id").val();
        $.post("/ec/rmv_prod/", {'prod_id':prod_id}, function(ret){
            location.reload();
        });
    })

    // 商品详情页增加商品数量
     $(".prod-qty-add").click(function () {
         qty = parseInt($(this).parent().children("input#id_qty").val());
         $(this).parent().children("input#id_qty").val( qty + 1);
    })

    // 商品详情页减少商品数量
    $(".prod-qty-del").click(function () {
        qty = parseInt($(this).parent().children("input#id_qty").val());
        if (qty == 1){
            $(this).attr("disabled",true);
        }
        else{
            $(this).parent().children("input#id_qty").val( qty - 1);
        }
    })

});