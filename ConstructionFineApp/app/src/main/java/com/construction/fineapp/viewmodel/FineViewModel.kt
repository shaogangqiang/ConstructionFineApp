package com.construction.fineapp.viewmodel

import android.app.Application
import android.graphics.Bitmap
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.construction.fineapp.api.ViolationAnalysis
import com.construction.fineapp.api.QwenApiService
import com.construction.fineapp.data.FineDatabase
import com.construction.fineapp.data.FineRecord
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream

data class FineUiState(
    val currentImage: Bitmap? = null,
    val selectedAmount: Int? = null,
    val isLoading: Boolean = false,
    val analysis: ViolationAnalysis? = null,
    val error: String? = null,
    val showHistory: Boolean = false
)

class FineViewModel(application: Application) : AndroidViewModel(application) {
    private val database = FineDatabase.getDatabase(application)

    private val _uiState = MutableStateFlow(FineUiState())
    val uiState: StateFlow<FineUiState> = _uiState.asStateFlow()

    private val _historyRecords = MutableStateFlow<List<FineRecord>>(emptyList())
    val historyRecords: StateFlow<List<FineRecord>> = _historyRecords.asStateFlow()

    private val _apiService: QwenApiService? by lazy {
        val apiKey = System.getenv("QWEN_API_KEY")
        if (apiKey != null) QwenApiService(apiKey) else null
    }

    init {
        loadHistory()
    }

    private fun loadHistory() {
        viewModelScope.launch {
            database.fineDao().getAllRecords().collect { records ->
                _historyRecords.value = records
            }
        }
    }

    fun captureImage(bitmap: Bitmap) {
        _uiState.value = _uiState.value.copy(
            currentImage = bitmap,
            analysis = null,
            error = null
        )
    }

    fun selectAmount(amount: Int) {
        _uiState.value = _uiState.value.copy(
            selectedAmount = amount
        )
    }

    fun analyzeImage(bitmap: Bitmap, apiKey: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(
                isLoading = true,
                error = null
            )

            val service = QwenApiService(apiKey)
            val result = service.analyzeImage(bitmap)

            result.fold(
                onSuccess = { analysis ->
                    _uiState.value = _uiState.value.copy(
                        analysis = analysis,
                        isLoading = false
                    )
                },
                onFailure = { exception ->
                    _uiState.value = _uiState.value.copy(
                        error = exception.message ?: "分析失败",
                        isLoading = false
                    )
                }
            )
        }
    }

    fun saveFineRecord(context: android.content.Context) {
        viewModelScope.launch {
            val state = _uiState.value
            val bitmap = state.currentImage ?: return@launch
            val amount = state.selectedAmount ?: return@launch
            val analysis = state.analysis ?: ViolationAnalysis(
                violation = "待补充",
                description = "待补充",
                suggestion = "待补充"
            )

            // Save image to file
            val imageFile = File(context.filesDir, "fine_${System.currentTimeMillis()}.jpg")
            FileOutputStream(imageFile).use { out ->
                bitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 80, out)
            }

            // Save to database
            val record = FineRecord(
                imagePath = imageFile.absolutePath,
                amount = amount,
                violation = analysis.violation,
                description = analysis.description,
                suggestion = analysis.suggestion
            )

            database.fineDao().insert(record)

            // Reset state
            _uiState.value = FineUiState()
        }
    }

    fun deleteRecord(id: Long) {
        viewModelScope.launch {
            database.fineDao().deleteById(id)
        }
    }

    fun toggleHistory() {
        _uiState.value = _uiState.value.copy(
            showHistory = !_uiState.value.showHistory
        )
    }

    fun clearCurrentImage() {
        _uiState.value = FineUiState()
    }
}
