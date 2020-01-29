from apps.projects.models import Experiment, Project, Datarow, Value

def project_serialize(project_id):
    #get all experiments from that project into a nested list of dictionaries to post to the selected webservice
    experiment_objects = list(Experiment.objects.filter(project=project_id))
    for experiment_object in experiment_objects:
        datarow_objects = list(Datarow.objects.filter(experiment=experiment_object.id))
        datarow_objects_list = []
        for datarow_object in datarow_objects:
            data_objects_list = list(Value.objects.filter(datarow=datarow_object.id).values_list('value', flat=True))
            #convert decimal values to string to make them serializable for json
            #for data_object in data_objects_list:
            #    data_object = str(data_object)
            data_objects_list = list(map(lambda x:str(x),data_objects_list))
            datarow_attributes = {
                'name' : datarow_object.name,
                'unit' : datarow_object.unit,
                'description' : datarow_object.description,
                'function_type' : datarow_object.function_type,
                'response_node' : datarow_object.response_node,
                'response_name' : datarow_object.response_name,
                'response_dir' : datarow_object.response_dir,
                'reference_node' : datarow_object.reference_node,
                'reference_name' : datarow_object.reference_name,
                'reference_dir' : datarow_object.reference_dir,
                'data_format' : datarow_object.data_format,
                'data_type' : datarow_object.data_type,
                'measuring_instrument' : datarow_object.measuring_instrument,
                'data': data_objects_list
            }
            datarow_objects_list.append(datarow_attributes)

        experiment_attributes = {
            'name': experiment_object.name,
            'description': experiment_object.description,
            'datarows': datarow_objects_list
        }
        input = experiment_attributes
        return input
