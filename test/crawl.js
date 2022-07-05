const $ = require('jquery')
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const axios = require('axios')

// const dom = new jsdom.JSDOM("")
// const $ = require('jquery')(dom.window)

URL = "https://uma.inven.co.kr/dataninfo/deckbuilder/"

const test = async() => {
    try{
        const response = await axios.get("https://uma.inven.co.kr/dataninfo/deckbuilder/")
        const {window} = new JSDOM(response.data)
        
        const paths = ['.umamusume-list', '.support-card-list']
        const types = ['umamusume', 'supportCard']

	    paths.forEach( (table, idx) => {
            const data = window.document.querySelectorAll('.container ' + table + ' .scroll-wrap ul li')
            data.forEach( (li) => _crawl(types[idx], li.getAttribute('data-code')) )
        })
    }
    catch(e){
        console.log(e)
    }
}

const _crawl = (type, code) => {
    try{
        const data = {
            "type": type,
            "code": code
        }
        const config = {
            headers:{
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "Data-Type": 'json'
            }
        }
        axios.post("https://uma.inven.co.kr/dataninfo/deckbuilder/detail.ajax.php?v=20220623a", data, config)
            .then(result => console.log(result.data))
            .catch(err => console.log(err))
        // $.ajax({
        //     url: "https://uma.inven.co.kr/dataninfo/deckbuilder/detail.ajax.php",
        //     type: "POST",
        //     data: {
        //         "type": type,
        //         "code": code
        //     },
        //     contentType: "application/x-www-form-urlencoded; charset=utf-8",
        //     dataType: 'json',
        //     //success: result => crawling_list[code] = result,
        //     //error: result => console.log(result)
        // }).done(result => crawling_list[code] = result);
    }
    catch(e){
        console.log(e)
    }
}

_crawl('umamusume', 102601)
// test()



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

// contentType: 'application/json', 으로 보내지 않도록 하자