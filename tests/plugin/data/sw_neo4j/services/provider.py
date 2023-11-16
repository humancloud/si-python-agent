#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#


if __name__ == '__main__':
    from fastapi import FastAPI
    import uvicorn
    import neo4j

    app = FastAPI()


    @app.get('/users')
    async def users():
        driver = neo4j.GraphDatabase.driver('bolt://neo4j:7687/')
        with driver.session(database='neo4j') as session:
            session.run('MATCH (n: stage) WHERE n.age=$age RETURN n', {'age': 10})

        with driver.session(database='neo4j') as session:
            with session.begin_transaction() as tx:
                tx.run('MATCH (n: stage) WHERE n.age=$age RETURN n', {'age': 10})

        driver.close()

        driver = neo4j.AsyncGraphDatabase.driver('bolt://neo4j:7687/')
        async with driver.session(database='neo4j') as session:
            await session.run('MATCH (n: stage) WHERE n.age=$age RETURN n', {'age': 10})

        async def transaction_func(tx, query, params):
            return await tx.run(query, params)

        async with driver.session(database='neo4j') as session:
            await session.execute_read(
                transaction_func, 'MATCH (n: stage) WHERE n.age=$age RETURN n', {'age': 10})

        await driver.close()

        return 'success'


    uvicorn.run(app, host='0.0.0.0', port=9091)
