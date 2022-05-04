import './styles/App.css';
import React, {useState} from 'react';
import ArticleFilter from "./components/ArticleFilter";
import ArticleModule from "./components/ArticleModule";
import ArticleService from "./API/ArticleService";

function App() {
  const [articles, setArticles] = useState({});
  const [timeConfig, setTimeConfig] = useState({fromTime: 1650990000, toTime: 1651072236});

  return (
    <div className="App">
      <ArticleFilter
          timeConfig={timeConfig}
          setTimeConfig={setTimeConfig}
          getArticlesFunction={ArticleService.getArticles}
          setArticles={setArticles}/>
      <hr style={{margin: '15px 0'}}/>
        <h1 style={{textAlign: 'center', marginTop: '20px'}}>
            Articles
        </h1>
      <hr style={{margin: '15px 0'}}/>
        {Object.keys(articles).length
        ? <ArticleModule articles={articles}/>
        : <h1 style={{textAlign: 'center'}}>No articles found</h1>
        }
    </div>
  );
}

export default App;
