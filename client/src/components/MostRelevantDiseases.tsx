import { IDisorder } from "./DisorderDisplayBox";

import { useLocation, Link } from "react-router-dom";

interface IRelevantDisease {
    disorder: IDisorder,
    score: number
}

export function MostRelevantDiseases() {

    const location = useLocation();
    const { disorders } = location.state as { disorders: IRelevantDisease[] };
    return (
        <div className="most-relevant-diseases">
            <Link to="/">Home</Link>
            <h1 className="most-relevant-diseases-header" >Most Relevant Diseases</h1>
            <div className="most-relevant-diseases-body">
                {disorders.map(disorder => (
                    <ResultDisplayTile {...disorder} />
                ))}
            </div>
        </div>
    );
}

function ResultDisplayTile(props: IRelevantDisease) {

    const relevantDisease = props;
    const disorder = relevantDisease.disorder;

    return(
        <div className="disorder-display-box-body-disorder" key={disorder.id}>
            <h2 className='disorder-name' >{disorder.name}</h2>
            <p className='disorder-metadata'>Disorder Type: {disorder.disorderType}</p>
            <p className='disorder-metadata'>Disorder Group: {disorder.disorderGroup}</p>
            <p className='disorder-metadata'>Orpha Code: {disorder.orphaCode}</p>
            <a className='disorder-metadata' href={disorder.expertLink.toString()}>More Details</a>
        </div>
    )
}