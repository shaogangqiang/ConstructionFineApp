package com.construction.fineapp.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface FineDao {
    @Insert
    suspend fun insert(record: FineRecord): Long

    @Query("SELECT * FROM fine_records ORDER BY timestamp DESC")
    fun getAllRecords(): Flow<List<FineRecord>>

    @Query("DELETE FROM fine_records WHERE id = :id")
    suspend fun deleteById(id: Long)

    @Query("SELECT * FROM fine_records ORDER BY timestamp DESC LIMIT :limit")
    fun getRecentRecords(limit: Int): Flow<List<FineRecord>>
}
