package com.construction.fineapp.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "fine_records")
data class FineRecord(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val imagePath: String,
    val amount: Int,
    val violation: String,
    val description: String,
    val suggestion: String,
    val timestamp: Long = System.currentTimeMillis()
)
