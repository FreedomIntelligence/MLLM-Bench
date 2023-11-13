
    $(document).ready(function () {
        // Handle the form submission
        var interval;  // for controlling the animation

        function animateButton() {
            var count = 0;
            interval = setInterval(function() {
                count++;
                var dots = ".".repeat(count % 4);  // creates '.', '..', '...', or ''
                $("#submit_button").text("Processing" + dots);
            }, 1000);
        }
    
        function stopButtonAnimation() {
            clearInterval(interval);
            $("#submit_button").text("2.Upload ＆ Process");
        }
    
        // Handle the form submission
        $("#uploadForm").submit(function (e) {
            e.preventDefault(); // Prevent default form submission
    
            animateButton(); // Start the animation
    
            // Create a FormData object to hold the file data
            var formData = new FormData(this);
    
            $.ajax({
                type: "POST",
                url: "https://cmedbenchmark.llmzoo.com/upload",
                data: formData,
                contentType: false,
                processData: false,
                success: function (response) {
                    stopButtonAnimation(); // Stop the animation
    
                    // Assuming the server returns a JSON with a 'path' attribute
                    var filePath = response;
                    var newPath = filePath.replace('/share/FILE_SERVER', 'https://file.huatuogpt.cn');

                    // 把newPath写到 id="result" 内，要注意保持换行
                    $.ajax({
                        type: "GET",
                        url: newPath,
                        success: function(result) {
                            var formattedJson = JSON.stringify(result, null, 4);
                            var formattedContent = formattedJson.replace(/\n/g, "<br>").replace(/ /g, "&nbsp;");
                            $("#result").html(formattedContent);
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            alert("Error fetching file content. Please try again.");
                        }
                    });
    
                    // Set the href attribute of the download link with the received file path
                    $("#download_result").attr("href", newPath);
                    $("#download_result").show();
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    stopButtonAnimation(); // Stop the animation
                    alert("Error uploading file. Please try again.");
                }
            });
        });

        

        document.getElementById('download_result').addEventListener('click', function(event) {
            event.preventDefault();  // 阻止默认的链接点击行为
        
            fetch(this.href)  // 请求文件
                .then(response => response.blob())
                .then(blob => {
                    const downloadUrl = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = downloadUrl;
                    a.download = "result.json";  // 您希望的文件名
                    document.body.appendChild(a);
                    a.click();
                    URL.revokeObjectURL(downloadUrl);  // 清理并释放URL
                    document.body.removeChild(a);
                });
        });

        // Function to update the filename input field when a file is selected
        function updateFilename() {
            var fileInput = document.getElementById("fileInput");
            var filenameInput = document.getElementById("filenameInput");
            if (fileInput.files.length) {
                filenameInput.value = fileInput.files[0].name;
            } else {
                filenameInput.value = "upload your file here";
            }
        }

        // Attach the function to the onchange event of the file input
        $("#fileInput").change(updateFilename);
    });