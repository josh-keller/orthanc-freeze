import time
from pydicom.uid import CTImageStorage
from pynetdicom import AE, evt, debug_logger
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelMove,
    PatientRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelMove,
)
from pydicom.dataset import Dataset

# Enable debugging
debug_logger()


def handle_c_find(event):
    """Handle a C-FIND request, returning a dummy study."""
    # Create a dummy dataset to return
    ds = Dataset()
    ds.PatientName = "Doe^John"
    ds.PatientID = "123456"
    ds.StudyInstanceUID = "1.2.840.10008.1.2.1"
    ds.StudyDescription = "Dummy Study"
    ds.StudyDate = "20230101"
    ds.ModalitiesInStudy = ["CT"]

    # Yield the dataset as a response
    yield 0xFF00, ds  # Pending status with dataset

    # Final response with status 'Success'
    yield 0x0000, None


def handle_c_move(event):
    """
    For any C-MOVE request:
    - Respond with a 'pending' status every 5 seconds,
    - Always indicate the same number of remaining sub-operations,
    - Never indicate progress towards completion.
    """
    yield "debug"


# Define the event handlers
handlers = [(evt.EVT_C_FIND, handle_c_find), (evt.EVT_C_MOVE, handle_c_move)]

# Initialize the Application Entity
ae = AE()

# Add supported presentation contexts
ae.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
ae.add_supported_context(StudyRootQueryRetrieveInformationModelFind)
ae.add_supported_context(StudyRootQueryRetrieveInformationModelMove)
ae.add_requested_context(CTImageStorage)
# Start the server
print("Starting 'bad' C-MOVE SCP on port 11112...")
ae.start_server(("0.0.0.0", 11112), block=True, evt_handlers=handlers)
