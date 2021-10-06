import numpy as np
import pandas as pd

def get_field_weights():
    fields_weights={'Age':3, 'Performance Status':6, 'Treatment Site':10, 'T':10,'N':10,'M':10,
                'Indications/Risk Group NCCN':10, 'Primary Site':10, 'Metastasis':10, 'No. of Nodes':10,'Histology/Pathology':10,
               'Margin':10,'PSA':10,'Gleason':10, 'Recurrence':10,
               'Treatment Intent':10, 'Retreat':10, 'Prior RT':10, 'Surgery':10, 'Other Therapies':10}
    return fields_weights

def get_protocol_map(protocol, fields_weights):
    '''protocol: protocol data
       field_weights: fields weights dict'''
    protocol_map={}
    for p in protocol['Study Name']:
        protocol_map[p]={}
        for f in fields_weights.keys():
            protocol_map[p][f]=protocol.loc[protocol['Study Name']==p, f].values[0]
    return protocol_map

def match(patient, fields, protocols, fields_to_match=None, protocols_to_match=None):
    '''patient: single patient data
       fields: fields weights dict
       protocols: protocol map dict
       fields_to_match: list of fields to be matched
       protocols_to_match: list of protocols to be matched'''
    
    if (fields_to_match==None) and (protocols_to_match==None):
        score={}
        for p in protocols.keys():
            score[p]=0
            
            for f in fields.keys():
                if patient[f].values[0]==protocols[p][f]:
                    score[p]+=fields[f]
                    
        score={k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
        return score
    
    elif (fields_to_match==None) and (protocols_to_match!=None):
        score={}
        for p in protocols_to_match:
            score[p]=0
            
            for f in fields.keys():
                if patient[f].values[0]==protocols[p][f]:
                    score[p]+=fields[f]
                    
        score={k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
        return score
    
    elif (fields_to_match!=None) and (protocols_to_match==None):
        score={}
        for p in protocols.keys():
            score[p]=0
            
            for f in fields_to_match:
                if patient[f].values[0]==protocols[p][f]:
                    score[p]+=fields[f]
                    
        score={k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
        return score
    
    else:
        score={}
        for p in protocols_to_match:
            score[p]=0
            
            for f in fields_to_match:
                if patient[f].values[0]==protocols[p][f]:
                    score[p]+=fields[f]
                    
        score={k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
        return score

def match_counts(patient, fields, protocols):
    '''patient: patient data
       fields: fields weights dict
       protocols: protocol map dict'''
    score={}
    for p in protocols.keys():
        
        score[f'matches_{p}']=0
        for f in fields.keys():
            if patient[f].values[0]==protocols[p][f]:
                
                score[f'matches_{p}']+=1
    score={k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
    #avg=sum(score.values())/len(score.values())
    #return avg
    return score

if __name__ == "__main__":
    patient_df=pd.read_excel('DATA for Students 2021.09.30.xlsx', sheet_name='patient', header=[1])
    protocol_df=pd.read_excel('DATA for Students 2021.09.30.xlsx', sheet_name='protocol', header=[1])

    fields_weights=get_field_weights()
    protocol_map=get_protocol_map(protocol_df, fields_weights)

    score=match(patient_df.iloc[[0]], fields_weights, protocol_map)
    print('default matching results:', score)

    print('-'*40)
    score_customized_fields=match(patient_df.iloc[[0]], fields_weights, protocol_map, fields_to_match=['Age','Performance Status','Treatment Site'])
    print('customized field matching results:', score_customized_fields)

    print('-'*40)
    score_customized_protocols=match(patient_df.iloc[[0]], fields_weights, protocol_map, protocols_to_match=['JAMA G9-10','RTOG 0126'])
    print('customized protocol matching results:', score_customized_protocols)

    print('-'*40)
    score_customized_both=match(patient_df.iloc[[0]], fields_weights, protocol_map, 
                                fields_to_match=['Age','Performance Status','Treatment Site'], 
                                protocols_to_match=['JAMA G9-10','RTOG 0126'])
    print('customized matching results:', score_customized_both)

    print('-'*40)
    counts=match_counts(patient_df, fields_weights, protocol_map)
    print('match counts:', counts)