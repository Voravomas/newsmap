import React from 'react';
import Article from "./UI/Article/Article";

const ArticleListByRegion = ({articles, regionTitle}) => {
    return (
        <div>
            <h2 style={{textAlign: 'center', marginTop: '20px'}}>
                {regionTitle}
            </h2>
            {articles.map((article, index) =>
                <Article key={article.article_id} number={index + 1} article={article}/>
            )}
        </div>
    );
};

export default ArticleListByRegion;