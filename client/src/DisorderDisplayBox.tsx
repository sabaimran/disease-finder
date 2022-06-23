/**
 * DisorderDisplayBox shows all of the available rare disorders.
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import * as api from './api';

export interface IDisorder {
    id: number,
    name: String,
    disorderType: String,
    disorderGroup: String,
    orphaCode: number,
    expertLink: String
}

export function DisorderDisplayBox() {

    // Get all of the disorders from the API
    const [disorders, setDisorders] = useState<IDisorder[]>([]);
    useEffect(() => {
        api.getDisorders().then(disorders => setDisorders(disorders));
    }, []);

    const [search, setSearch] = useState('');

    return(
        <div className="disorder-display-box">
            <Link to="/">Home</Link>
            <div className="disorder-display-box-header">
                <h1 className='disorder-display-box-header' >Disorder Display Box</h1>
                <input type="text" placeholder="Search" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
            <div className="disorder-display-box-body">
                {disorders.filter(d => d.name.toLowerCase().includes(search.toLowerCase())).map(disorder => (
                    <DisorderDisplayTile {...disorder} />
                ))}
            </div>
        </div>
    )
}

function DisorderDisplayTile(props: IDisorder) {

    const disorder = props;

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
