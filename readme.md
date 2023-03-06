# PrivaTO-DO

This api is a **TODO list** and **note-taking**. The main difference of this app is that the tasks are
stored in a [blockchain](https://builtin.com/blockchain) that creates a history with all the changes and modifications
of the different notes/tasks.

## How it works?

This api allows the user add new notes and mark them as completed. The flow is always the same, first we need to add new
note/task and then these are saved on the Blockchain. In order to make the blockchain data persistent we need to store
Blockchain in a file. For this API, the Blockchain is store in a MongoDB database.

### Workflow

The workflow of the api is as follows:

1. Send request to the API to **add** or **mark as completed** any task.
2. Load the _Blockchain_ data from the file, if exists
3. Create a _Block_ with the new todo/task data
4. Add the new Block to the _Blockchain_
5. Save the Blockchain with the new data on a file

## Technical Considerations

Keep in mind the following:

1. Related with the blockchain:
    1. Every Block has multiple properties:
        1. `timestamp`: the timestamp for the moment when the block was created
        2. `lastHash`: hash of the previous block on the Blockchain
        3. `data`: information we want to store in the block (in our case the description of the task)
        4. `hash`: a SHA256 string for the block, calculated concatenating the timestamp, lastHash and data.
    2. The implementation of the Blockchain must follow these contract:
    ```
    interface Blockchain {
      /** Adds new block to blockchain */
      addBlock(block: Block): Block
      /**
       * Validates the chain by checking if:
       * - every element's last hash value matches previous block's hash
       * - data hasn't been tampered (which will produce a different hash value)
       */
      isValid(blockchain: Blockchain): boolean
      /** The new blockchain that is a candidate for replacing the current blockchain */
      replace(blockchain: Blockchain): boolean
    }

    interface Block {
      /** Generate the hash for the given block */
      static generateHashFromBlock(block: Block): string
    }
    ```

### How it works

#### - To add o mark as completed any task

To add a new task it must be used the /tasks/task HTTP POST request, with a JSON body showing the task data:

```
{
  "data": "info"
}
```

To mark a task as completed we use the /tasks/task HTTP PUT request, where a JSON body specify the task data:

```
{
  "data": "task",
  "id_hash": "any",
  "timestamp": "today",
  "last_hash": "last task id_hash",
  "completed": true
}
```

#### - Loading the Blockchain

To load the blockchain with the aim of showing the task list, we use the /tasks HTTP GET request

#### - To replace the blockchain

To replace the whole blockchain we use the /tasks HTTP PUT request, where a JSON body specify the new blockchain:

```
[
  {
    "id_hash": "214bcaf84e330fa9f925b17277f89979a344df27d7641002b206c7247957a3b6",
    "timestamp": "yesterday",
    "data": "test",
    "last_hash": "asdasdasdasd",
    "completed": false
  },
  {
    "id_hash": "70e6e36695fa9d281dab273aed64d93fc7a8a79a7bc000ddf77c249000006053",
    "timestamp": "today",
    "data": "test",
    "last_hash": "214bcaf84e330fa9f925b17277f89979a344df27d7641002b206c7247957a3b6",
    "completed": false
  }
]
```

#### - Important

Everytime that we send a request, the API checks if the present blockchain is valid or not. 
You can read the API swagger documentation in the /docs path.

### Testing the API
To run the API in a local server it uses "uvicorn", so run the command below in the terminal:
```
uvicorn app.main:app --reload
```

As the API uses a MongoDB database, a local database must be started in the machine.
It is also possible to use a remote database specifying the remote url in the client.py file
