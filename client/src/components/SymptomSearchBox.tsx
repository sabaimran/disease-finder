/**
 * SymptomSearchBox shows all of the available symptoms.
 */

import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import * as api from '../api';

export interface ISymptom {
    id: number,
    name: String,
    hpoId: String
}

export function SymptomSearchBox() {

    // Get all of the symptoms from the API
    const [symptoms, setSymptoms] = useState<ISymptom[]>([]);
    useEffect(() => {
        api.getSymptoms().then(symptoms => setSymptoms(symptoms));
    }, []);

    const [search, setSearch] = useState('');

    // Keep state of which symptoms are selected
    const [selectedSymptoms, setSelectedSymptoms] = useState<ISymptom[]>([]);

    let navigate = useNavigate();

    function searchBySymptoms() {
        // Get all of the disorders from the API
        api.findRelevantDiseaseBySymptoms(selectedSymptoms.map(s => s.id))
            .then(disorders => {
                console.log(disorders);
                navigate('/results', { state: { disorders } });
            });
    }

    return(
        <div className="symptom-display-box">
            <Link to="/">Home</Link>
            <div className="symptom-display-box-header">
                <h1 className='symptom-display-box-header'>Symptoms Search Page - Find Relevant Diseases</h1>
                <input type="text" placeholder="Search" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
            {/* Display the selected symptoms */}
            <h2 className="selected-symptoms-body-title">Selected Symptoms</h2>
            <div className="selected-symptoms-body">
                {selectedSymptoms.map(symptom => (
                    <div className="selected-symptoms-body-symptom" key={symptom.id}>
                        <h2 className='selected-symptoms-symptom-name' >{symptom.name}</h2>
                        <p className='selected-symptoms-symptom-metadata'>HPO ID: {symptom.hpoId}</p>
                        <button className='selected-symptoms-symptom-metadata' onClick={() => setSelectedSymptoms(selectedSymptoms.filter(s => s.id !== symptom.id))}>Remove</button>
                    </div>
                ))}
            </div>
            {/* Search for the most relevant diseases based on the selected symptoms */}
            {selectedSymptoms.length > 0 && 
                <button className="selected-symptoms-symptom-search" onClick={() => searchBySymptoms()}>Find Relevant Disorders</button>
            }
            {/* Display the list of all possible symptoms */}
            <h2 className="symptom-display-box-body-title">Symptom Options</h2>
            <div className="symptom-display-box-body">
                {symptoms.filter(s => (s.name.toLowerCase().includes(search.toLowerCase()) || s.hpoId.toLowerCase().includes(search.toLowerCase())) && !selectedSymptoms.find(s1 => s1.id === s.id)).map(symptom => (
                    <div className="symptom-display-box-body-symptom" key={symptom.id}>
                        <h2 className='symptom-name' >{symptom.name}</h2>
                        <p className='symptom-metadata'>HPO ID: {symptom.hpoId}</p>
                        <button className='symptom-metadata' onClick={() => {
                            // If the symptom is already selected, do nothing
                            if (!selectedSymptoms.find(s => s.id === symptom.id)) {
                                setSelectedSymptoms([...selectedSymptoms, symptom]);
                            }
                        }}>Add Symptom</button>
                    </div>
                ))}
            </div>
        </div>
    )
}
