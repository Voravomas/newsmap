import './styles/App.css';
import React, {useState} from 'react';

import ArticleFilter from "./components/ArticleFilter/ArticleFilter";
import ArticleModule from "./components/ArticleModule";
import ArticleService from "./API/ArticleService";
import Map from "./components/Map";
import Article from "./components/UI/Article/Article";
import OBLAST_TO_NUM from "./constants";
import ArticleListByRegion from "./components/ArticleListByRegion";

function App() {
  const [articles, setArticles] = useState([{
        article_id: "7342254",
        title: "Контактна група з оборони України засідатиме щомісяця - міністр оборони США",
        news_provider_name: "Pravda",
        article_type: "Pravda",
        link: "https://www.pravda.com.ua/news/2022/04/26/7342254/",
        time_published: "2022-04-26 19:45:00",
        published_timestamp: 1650991500,
        time_collected: "2022-04-26 20:14:03.645043",
        text_language: "UA",
        tags: [],
        regions: {
        10: {confidence: 1, places: ["Київ"]},
        14: {confidence: 0.5, places: ["Київ"]}
    }},
      {
          article_id: "686331",
          title: "Mercedes-Benz недоотримав 700 мільйонів євро прибутку через вихід з Росії",
          news_provider_name: "Pravda",
          article_type: "economyPravda",
          link: "https://www.epravda.com.ua/news/2022/04/27/686331/",
          time_published: "2022-04-27 18:34:00",
          published_timestamp: 1651073640,
          time_collected: "2022-04-27 18:46:23.714361",
          text_language: "UA",
          tags: [
              "автомобілі",
              "Німеччина",
              "Росія",
              "витрати"
          ],
          regions: {
              6: {confidence: 0.5, places: ["Прибуток"]}
          }}
  ]);
  const [timeConfig, setTimeConfig] = useState({fromTime: 1650990000, toTime: 1651072236});

    const data = [
        ['ua-my', 10], ['ua-ks', 11], ['ua-kc', 12], ['ua-zt', 13],
        ['ua-sm', 14], ['ua-dt', 15], ['ua-dp', 16], ['ua-kk', 17],
        ['ua-lh', 18], ['ua-pl', 19], ['ua-zp', 20], ['ua-sc', 21],
        ['ua-kr', 22], ['ua-ch', 23], ['ua-rv', 24], ['ua-cv', 25],
        ['ua-if', 26], ['ua-km', 27], ['ua-lv', 28], ['ua-tp', 29],
        ['ua-zk', 30], ['ua-vo', 31], ['ua-ck', 32], ['ua-kh', 33],
        ['ua-kv', 34], ['ua-mk', 35], ['ua-vi', 36]
    ];

    return (
    <div className="App">
      <ArticleFilter
          timeConfig={timeConfig}
          setTimeConfig={setTimeConfig}
          getArticlesFunction={ArticleService.getArticles}
          setArticles={setArticles}/>
      <div className="Map_and_article">
          <div>
              <Map data={data}/>
          </div>
          <div>
              <ArticleListByRegion
                  articles={articles}
                  regionTitle={"Mykolaiv"}/>
          </div>
      </div>


      {/*<hr style={{margin: '15px 0'}}/>*/}
      {/*  <h1 style={{textAlign: 'center', marginTop: '20px'}}>*/}
      {/*      Articles*/}
      {/*  </h1>*/}
      {/*<hr style={{margin: '15px 0'}}/>*/}
      {/*  {Object.keys(articles).length*/}
      {/*  ? <ArticleModule articles={articles}/>*/}
      {/*  : <h1 style={{textAlign: 'center'}}>No articles found</h1>*/}
      {/*  }*/}
    </div>
  );
}

export default App;
