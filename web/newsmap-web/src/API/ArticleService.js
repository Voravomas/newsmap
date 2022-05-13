import axios from "axios";

export default class ArticleService {
    static async getTotalArticles(from_time, to_time) {
        const fin_url = 'http://localhost:8000/articles/total/' + from_time + '/' + to_time;
        console.log("Sending request for getting total articles: ")
        console.log(from_time, to_time);
        const response = await axios.get(fin_url, {crossDomain: true});
        const article_data = response.data;
        console.log(article_data['response']);
        return article_data['response']
    }

    static async getArticlesByRegion(from_time, to_time,
                                     region, limit, offset) {
        const fin_url = 'http://localhost:8000/articles/';
        console.log("Sending request for getting article in region " + region)
        console.log(from_time, to_time);
        console.log(limit, offset);
        const response = await axios.post(fin_url, {
            crossDomain: true,
            from_time: from_time,
            to_time: to_time,
            region: region,
            limit: limit,
            offset: offset
        });
        const article_data = response.data;
        console.log(article_data['response']);
        return article_data['response']
    }
}