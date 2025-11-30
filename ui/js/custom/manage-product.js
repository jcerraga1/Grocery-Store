let productModal = $("#productModal");
    $(function () {

        //JSON data by API call
        $.get(productListApiUrl, function (response) {
            if(response) {
                let table = '';
                $.each(response, function(index, product) {
                    table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                        '<td style="display: none">'+ product.product_id +'</td>'+
                        '<td>'+ product.name +'</td>'+
                        '<td>'+ product.uom_name +'</td>'+
                        '<td>'+ product.price_per_unit +'</td>'+
                        '<td><span class="btn btn-xs btn-danger delete-product">Delete</span>&nbsp &nbsp &nbsp'+
                        '<span class="btn btn-xs btn-primary edit-product">Edit</span></td></tr>';
                });
                $("table").find('tbody').empty().html(table);
            }
        });
    });

    // Save Product
    $("#saveProduct").on("click", function () {
        let data = $("#productForm").serializeArray();
        let requestPayload = {
            product_id: null,       // add this
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };

        for (let i=0; i<data.length; ++i) {
            let element = data[i];
            switch(element.name) {
                case 'id':
                    requestPayload.product_id = element.value;
                    break;
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.price_per_unit = element.value;
                    break;
            }
        }

        // Decide whether to insert or update
        if (requestPayload.product_id && requestPayload.product_id !== "0") {
            // Update existing product
            callApi("POST", productUpdateApiUrl, {
                'data': JSON.stringify(requestPayload)
            });
        } else {
            // Insert new product
            callApi("POST", productSaveApiUrl, {
                'data': JSON.stringify(requestPayload)
            });
        }
    });


    $(document).on("click", ".delete-product", function (){
        let tr = $(this).closest('tr');
        let data = {
            product_id : tr.data('id')
        };
        let isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    $(document).on("click", ".edit-product", function() {
      const row = $(this).closest("tr");
      const id = row.find("td:eq(0)").text();
      const name = row.find("td:eq(1)").text();
      const unitName = row.find("td:eq(2)").text(); // UOM name from table
      const price = row.find("td:eq(3)").text();

      $("#id").val(id);
      $("#name").val(name);
      $("#price").val(price);

      // Stash the unit name on the modal for later use
      productModal.data("unitName", unitName);

      productModal.find(".modal-title").text("Edit Product");
      productModal.modal("show");
    });

    // Modal show: populate UOMs and select the matching one
    productModal.on("show.bs.modal", function() {
      $.get(uomListApiUrl, function(response) {
        if (!response) return;

        // Build options
        let options = '<option value="">--Select--</option>';
        $.each(response, function(_, uom) {
          options += '<option value="' + uom.uom_id + '">' + uom.uom_name + '</option>';
        });
        $("#uoms").empty().html(options);

        // Map unit name → id, then select by value
        const unitName = (productModal.data("unitName") || "").trim().toLowerCase();
        if (unitName) {
          const match = response.find(u =>
            (u.uom_name || "").trim().toLowerCase() === unitName
          );
          if (match) {
            $("#uoms").val(match.uom_id).trigger("change"); // select by ID
          }
        }
      });
    });

    // Modal hide: reset for Add Product flow
    productModal.on("hide.bs.modal", function() {
      $("#id").val("0");
      $("#name, #price").val("");
      $("#uoms").val("");
      productModal.removeData("unitName");
      productModal.find(".modal-title").text("Add New Product");
    });

