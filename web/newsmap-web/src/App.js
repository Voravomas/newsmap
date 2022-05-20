import './styles/App.css';
import React, {useState} from 'react';

import ArticleFilter from "./components/ArticleFilter/ArticleFilter";
import Map from "./components/Map";
import ArticleListByRegion from "./components/ArticleListByRegion";
import region_data from "./regions.json";

function App() {
  const [totalArticles, setTotalArticles] = useState(region_data);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [articles, setArticles] = useState([]);
  const [requestOffset, setRequestOffset] = useState(0);
  const [timeConfig, setTimeConfig] = useState({fromTime: 1645660800, toTime: 1677196800});

    return (
    <div className="App">
      <ArticleFilter
          timeConfig={timeConfig}
          totalArticles={totalArticles}
          setTimeConfig={setTimeConfig}
          setArticles={setArticles}
          setSelectedRegion={setSelectedRegion}
          setTotalArticles={setTotalArticles}/>
      <div className="Map_and_article">
          <div>
              <Map
                  totalArticles={totalArticles}
                  setSelectedRegion={setSelectedRegion}
                  setArticles={setArticles}
                  timeConfig={timeConfig}
                  setRequestOffset={setRequestOffset}
              />
          </div>
          <div>
              <ArticleListByRegion
                  articles={articles}
                  selectedRegion={selectedRegion}
                  setArticles={setArticles}
                  requestOffset={requestOffset}
                  setRequestOffset={setRequestOffset}
                  timeConfig={timeConfig}
                  totalArticlesInRegion={selectedRegion ? totalArticles[selectedRegion - 1].numArticles : null}
              />
          </div>
      </div>
    </div>
  );
}

export default App;
