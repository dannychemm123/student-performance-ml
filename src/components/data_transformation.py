import sys
import pandas as pd
from dataclasses import dataclass
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from src.logger import logging
from src.exception import CustomException
import os
from src.utils import save_object

class DataTransformationnConfig:
    ''' The configuration for the data transformation '''
    preprocessor_obj_file_path = os.path.join('artifacts', 'proprocessor.pkl')
    
class DataTransformation:
    ''' The data transformation class'''
    def __init__(self):
        ''''initialize data transformation class'''
        self.data_transformation_config = DataTransformationnConfig()
    def get_data_transformer_objects(self):
        '''This function is responsible for data transformation and preparing 
        data based on whether categorical features or numerical features'''
        try:
            numerical_columns = ['writing_score','reading_score',]
            categorical_columns = ['gender',
                                   'race_ethnicity',
                                   'parental_level_of_education',
                                   'lunch',
                                   'test_preparation_course']
            num_pipeline = Pipeline(
                steps=[
                    ('inputer',SimpleImputer(strategy = 'median',)),
                    ('scaler',StandardScaler())
                ]
                
            )
            cat_pipeline = Pipeline(
                steps=[
                    ('inputer',SimpleImputer(strategy = 'most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
                )
            logging.info('Numerical colums standard scaling completed successfully')
            logging.info('Categorical columns encoding completed successfully')
            
            preprossor =ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns),
                    
                ]
            )
            return preprossor
        
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            

            logging.info('Train data and test data reading is completed' )
            logging.info('Obtaning preprocessing Objects')
            preprocessing_objects = self.get_data_transformer_objects()
            
            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']
            
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis= 1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name],axis= 1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info(" Applying preprocessing object on training and testing dataframe")
            input_feature_train_array = preprocessing_objects.fit_transform(input_feature_train_df)
            input_feature_test_array =  preprocessing_objects.transform(input_feature_test_df)
            
            
            
            train_array = np.c_[
                input_feature_train_array,np.array(target_feature_train_df)
            ]
            test_array = np.c_[input_feature_test_array,np.array(target_feature_test_df)]
            
            logging.info('Saved processing object successfully')
            
            save_object(
                file_path  = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_objects
            )
            
            return (
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)
    