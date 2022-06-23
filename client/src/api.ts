import { IDisorder } from "./components/DisorderDisplayBox";
import { ISymptom } from "./components/SymptomSearchBox";

const API_URL = 'http://localhost:5000';

export async function getDisorders() {
    const response = await fetchWrapper('disorders', 'GET');
    const data = await response.json();
    return data['disorders'] as IDisorder[];
}

export async function getSymptoms() {
    const response = await fetchWrapper('symptoms', 'GET');
    const data = await response.json();
    return data['symptoms'] as ISymptom[];
}

export async function findRelevantDiseaseBySymptoms(symptomIds: number[]) {
    let body = {
        "symptomIds": symptomIds
    };

    const response = await fetchWrapper(
        'find-disorders',
        'POST',
        JSON.stringify(body));

    const data = await response.json();
    return data['disorders'] as IDisorder[];
}

function fetchWrapper(endpoint: string, method: string, body?: any) {
    return fetch(`${API_URL}/${endpoint}`, {
        method: method,
        body: body,
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
    });
}
