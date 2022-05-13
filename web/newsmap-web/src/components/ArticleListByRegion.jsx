import React from 'react';
import Article from "./UI/Article/Article";
import RegionNameWithButtons from "./UI/RegionNameWithButtons/RegionNameWithButtons";
import {DEFAULT_LIMIT} from "../constants";

const ArticleListByRegion = ({articles, selectedRegion, setArticles, requestOffset,
                                setRequestOffset, timeConfig, totalArticlesInRegion}) => {
    function countPageString(curOffset, totalArticles) {
        if (curOffset === null || totalArticles === null ||
            curOffset === undefined || totalArticles === undefined) {
            return ''
        }
        let maxPage = Math.ceil(totalArticles / DEFAULT_LIMIT);
        let curPage = curOffset / DEFAULT_LIMIT + 1;
        return 'Page ' + curPage + ' / ' + maxPage;
    }

    return (
        <div>
            <RegionNameWithButtons
                setArticles={setArticles}
                setRequestOffset={setRequestOffset}
                requestOffset={requestOffset}
                selectedRegion={selectedRegion}
                timeConfig={timeConfig}
                totalArticlesInRegion={totalArticlesInRegion}
            />
            <hr style={{margin: '15px 0'}}/>
            {articles.length === 0
                ? <h2>Немає статей по регіону</h2>
                : articles.map((article, index) => <Article key={article.article_id} number={index + 1} article={article}/>)
            }
            <hr style={{margin: '15px 0'}}/>
            {articles.length === 0
                ? <p></p>
                : <p>{countPageString(requestOffset, totalArticlesInRegion)}</p>
            }
        </div>
    );
};

export default ArticleListByRegion;