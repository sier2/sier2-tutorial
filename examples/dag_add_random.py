from sier2 import Library

def main():
    add_dag = Library.get_dag('sier2_tutorial.dags:example_add_dag')
    add_dag.execute()

    result = add_dag.block_by_name('result').out_result
    print(f'{result=}')

if __name__=='__main__':
    main()
