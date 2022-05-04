import axios from "axios";

export default class ArticleService {
    static async getArticles(from_time, to_time) {
        const fin_url = 'http://localhost:8000/articles/' + from_time + '/' + to_time;
        console.log(from_time, to_time);
        const response = await axios.get(fin_url, {crossDomain: true});
        const all_article_data = response.data;
        console.log(all_article_data['articles']);
        return all_article_data['articles']
    }
}