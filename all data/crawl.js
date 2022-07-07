location.href = "https://uma.inven.co.kr/dataninfo/deckbuilder/"

let crawl = () => {
    let crawling_list = {}
    const types = ['umamusume', 'supportCard']
    const paths = ['.umamusume-list', '.support-card-list']
    paths.forEach( (path, idx) => {
        $('.container ' + path + ' .scroll-wrap ul li').each((_, code) => {
            $.ajax({
                url: "detail.ajax.php",
                type: "POST",
                data: {
                    "type": types[idx],
                    "code": $(code).attr('data-code')
                },
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                dataType: 'json',
                success: result => crawling_list[$(code).attr('data-code')] = result,
                error: result => console.log(result)
            });
        })
    })
    console.log(crawling_list)
}