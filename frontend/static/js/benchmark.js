$(document).ready(function () {

    let models = [
        "blip2-flan-t5-xl.json",
        "fuyu-8b.json",
        "instructblip-vicuna-13b.json",
        "llava-v1.5-13b.json",
        "minigpt-v2.json",
        "qwen-vl-chat.json",
        "cogvlm-chat.json",
        "idefics-9b-instruct.json",
        "kosmos-2.json",
        "lvis-instruct4v-llava-7b.json",
        "mPLUG-owl2.json",
        "seed-llama-14b.json",
    ]
    // 初始化计数器
    let jsonFilesLoaded = 0;
    let jsonDataCache = {};
    // 加载所有的结果文件
    $(document).ready(function () {
        // 预加载所有的JSON文件
        models.forEach(function (model) {
            var modelName = model.replace('.json', '');
            var jsonUrl = "https://file.huatuogpt.cn/files/models_ref/mllm/data/answers/v1/" + modelName + ".json";

            $.getJSON(jsonUrl, function (data) {
                jsonDataCache[jsonUrl] = data;
                jsonFilesLoaded++;

                // 当所有文件都加载完毕时，调用 showSelectedValues
                if (jsonFilesLoaded === models.length) {
                    showSelectedValues();
                }

            });
        });

    });

    // 定义一个函数来填充第二个下拉框
    function updateDropdown2(data) {
        let selectedLevel = $('#dropdown1').val();
        let questions = data.filter(item => item.meta.level === selectedLevel).map(item => item.id + ":" + item.question);

        let dropdown2 = $('#dropdown2');
        dropdown2.empty();
        $.each(questions, function (index, question) {
            dropdown2.append($('<option>', {value: question, text: question}));
        });
    }

    // 更新contentDisplay的函数
    function updateContentDisplay(item) {
        $('#contentDisplay').empty();
        $('#contentDisplay').append('<p><strong>User</strong></p>');
        $('#contentDisplay').append('<p>' + item.question + '</p>');
        $('#contentDisplay').append('<img src="' + item.image_path + '" style="max-width:95%; height:auto;">');
    }

    // 异步加载JSON文件
    $.getJSON('https://file.huatuogpt.cn/files/models_ref/mllm/data/questions/vllm_bench_v1.json', function (data) {
        let levels = new Set(); // 用于存储唯一的level值

        // 遍历JSON数据，填充levels集合
        $.each(data, function (index, item) {
            levels.add(item.meta.level);
        });

        let levelsArray = Array.from(levels);

        // 填充第一个下拉框
        $.each(levelsArray, function (index, level) {
            $('#dropdown1').append($('<option>', {value: level, text: level}));
        });

        // 默认填充第二个下拉框
        updateDropdown2(data)
        updateContentDisplay(data[0])

        // 当第一个下拉框的选项改变时
        $('#dropdown1').change(function () {
            let selectedLevel = $(this).val();
            let questions = data.filter(item => item.meta.level === selectedLevel).map(item => item.id + ":" + item.question);

            // 清空并填充第二个下拉框
            $('#dropdown2').empty();
            $.each(questions, function (index, question) {
                $('#dropdown2').append($('<option>', {value: question, text: question}));
            });

            // 更新contentDisplay
            let firstItem = data.find(item => item.meta.level === selectedLevel);
            if (firstItem) updateContentDisplay(firstItem);

        });

        // 当第二个下拉框的选项改变时
        $('#dropdown2').change(function () {
            let selectedId = $(this).val().split(':')[0];
            let selectedItem = data.find(item => item.id == selectedId);
            if (selectedItem) updateContentDisplay(selectedItem);
            // 获取answer
            showSelectedValues()
        });

        // 初始结果
        showSelectedValues();
    });

    // 填充第三个下拉框
    $(document).ready(function () {
        models.forEach(function (model) {
            let modelName = model.replace('.json', '');
            $('#dropdown3').append(new Option(modelName, modelName));
        });
    });


    function showSelectedValues() {
        let dropdown2Value = $('#dropdown2').val().split(':')[0];
        let dropdown3Value = $('#dropdown3').val();

        // 构造JSON文件的URL
        var jsonUrl = "https://file.huatuogpt.cn/files/models_ref/mllm/data/answers/v1/" + dropdown3Value + ".json";

        if (jsonDataCache[jsonUrl]) {
            displayData(jsonDataCache[jsonUrl], dropdown2Value);
        } else {
            // 如果没有缓存数据，则显示错误信息
            $('#resultDisplay').html("Failed to load data.");
        }
    }

    function displayData(data, dropdown2Value) {
        var foundItem = data.find(item => item.unique_idx == dropdown2Value);
        if (foundItem) {
            $('#resultDisplay').empty();
            $('#resultDisplay').append('<p><strong>Assistant</strong></p>');
            let formattedAnswer = foundItem.answer.replace(/\n/g, '<br>');
            $('#resultDisplay').append('<p>' + formattedAnswer + '</p>');
        } else {
            $('#resultDisplay').html("Match not found.");
        }
    }

    // 当第二个下拉框的选项改变时
    $('#dropdown3').change(function () {
        // 获取answer
        showSelectedValues()
    });

});
